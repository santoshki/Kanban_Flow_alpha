from flask import Flask, render_template, request, redirect, url_for, jsonify
from database.sqldb import get_db, close_db, init_db, insert_project
from datetime import datetime, date
import calendar

app = Flask(__name__)


@app.route('/')
def home():
    db = get_db()
    today = datetime.today().strftime('%Y-%m-%d')

    active_projects = db.execute(
        "SELECT COUNT(*) FROM projects WHERE end_date IS NULL OR end_date > ?", (today,)
    ).fetchone()[0]

    closed_projects = db.execute(
        "SELECT COUNT(*) FROM projects WHERE end_date IS NOT NULL AND end_date <= ?", (today,)
    ).fetchone()[0]

    return render_template(
        'home.html',
        active=active_projects,
        closed=closed_projects,
        active_page='home'
    )


@app.route('/projects')
def projects():
    db = get_db()
    projects = db.execute("SELECT * FROM projects ORDER BY start_date DESC").fetchall()
    return render_template('projects.html', projects=projects, active_page='projects')


@app.route('/calendar')
def calendar_view():
    today = date.today()
    year = today.year
    months_data = []

    for month in range(1, 13):
        first_weekday, total_days = calendar.monthrange(year, month)
        month_name = date(year, month, 1).strftime('%B')
        months_data.append({
            "month": month,
            "year": year,
            "month_name": month_name,
            "first_weekday": first_weekday,
            "total_days": total_days
        })

    return render_template("calendar.html", current_date=today, months_data=months_data)


@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)


@app.route('/new_project', methods=['GET', 'POST'])
def new_project():
    if request.method == 'POST':
        project_name = request.form.get('project-name')
        project_description = request.form.get('project-description')
        project_poc = request.form.get('project-POC')
        project_start_date = request.form.get('startDate')
        project_end_date = request.form.get('endDate')
        if project_name:
            insert_project(project_name, project_description, project_poc, project_start_date, project_end_date)
            return redirect(url_for('project_detail', project_name=project_name))
    return render_template('new_project.html', active_page='projects')


@app.route('/project/<project_name>')
def project_detail(project_name):
    db = get_db()
    project = db.execute('SELECT * FROM projects WHERE name = ?', (project_name,)).fetchone()
    if not project:
        return "Project not found", 404

    tasks = db.execute('SELECT * FROM tasks WHERE project_id = ? ORDER BY id', (project['id'],)).fetchall()
    task_list = []

    for task in tasks:
        comments = db.execute('SELECT * FROM comments WHERE task_id = ? ORDER BY timestamp', (task['id'],)).fetchall()
        task_dict = dict(task)
        task_dict['comments'] = comments
        task_list.append(task_dict)

    return render_template('project_detail.html', project_name=project_name, tasks=task_list, active_page='projects')


@app.route('/project/<project_name>/add_task', methods=['POST'])
def add_task(project_name):
    db = get_db()
    project = db.execute('SELECT * FROM projects WHERE name = ?', (project_name,)).fetchone()
    if not project:
        return "Project not found", 404

    title = request.form.get('title')
    description = request.form.get('description')
    start_date = request.form.get('start_date')
    due_date = request.form.get('due_date')
    assignee = request.form.get('assignee')
    priority = request.form.get('priority', '').capitalize()

    if priority not in ('Low', 'Medium', 'High'):
        return "Invalid priority value", 400

    status = 'To Do'

    if not title or not priority or not start_date:
        return "Missing required task data", 400

    db.execute('''
        INSERT INTO tasks (project_id, title, description, status, priority, start_date, due_date, assignee)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (project['id'], title, description, status, priority, start_date, due_date, assignee))
    db.commit()

    return redirect(url_for('project_detail', project_name=project_name))


@app.route('/add_comment/<int:task_id>', methods=['POST'])
def add_comment(task_id):
    db = get_db()
    author = request.form.get('author')
    content = request.form.get('content')

    if not author or not content:
        return "Missing comment data", 400

    db.execute('''
        INSERT INTO comments (task_id, author, content)
        VALUES (?, ?, ?)
    ''', (task_id, author, content))
    db.commit()

    task = db.execute('SELECT project_id FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if task:
        project = db.execute('SELECT name FROM projects WHERE id = ?', (task['project_id'],)).fetchone()
        return redirect(url_for('project_detail', project_name=project['name']))
    return "Task not found", 404


@app.route('/update_task/<int:task_id>', methods=['POST'])
def update_task_route(task_id):
    db = get_db()
    form = request.form

    fields = ['title', 'description', 'start_date', 'due_date', 'assignee', 'priority']
    for field in fields:
        value = form.get(field)
        db.execute(f'UPDATE tasks SET {field} = ? WHERE id = ?', (value, task_id))

    author = form.get('comment_author')
    content = form.get('comment_content')
    print("Comments added:")
    print("Author:", author)
    print("Comment:", content)
    if author and content:
        db.execute(
            'INSERT INTO comments (task_id, author, content) VALUES (?, ?, ?)',
            (task_id, author, content)
        )

    db.commit()
    return redirect(url_for('project_detail', project_name=request.args.get('project_name')))


@app.route('/get_task/<int:task_id>')
def get_task(task_id):
    db = get_db()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if not task:
        return jsonify(error='not found'), 404

    comments = db.execute('SELECT * FROM comments WHERE task_id = ? ORDER BY timestamp', (task_id,)).fetchall()

    task_data = dict(task)
    task_data['comments'] = [dict(c) for c in comments]

    return jsonify(task_data)


@app.route('/update_task_status/<int:task_id>', methods=['POST'])
def update_task_status(task_id):
    db = get_db()
    data = request.get_json()
    app.logger.info(f"Received status update for task {task_id}: {data}")

    if not data or 'status' not in data:
        return jsonify({'error': 'Missing status'}), 400

    new_status = data['status']

    if new_status not in ('To Do', 'In Progress', 'Done'):
        return jsonify({'error': 'Invalid status'}), 400

    try:
        db.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id))
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        app.logger.error(f'Error updating task status in DB: {e}')
        return jsonify({'error': 'Failed to update task status'}), 500


@app.route('/users')
def users():
    db = get_db()
    rows = db.execute("SELECT name FROM projects ORDER BY start_date DESC").fetchall()
    projects = [row['name'] for row in rows]
    return render_template('new_users.html', projects=projects)


@app.route('/settings')
def settings():
    print("Stay tuned for more details")
    return render_template('settings.html')


if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run(debug=True)
