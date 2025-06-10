from flask import Flask, render_template, request, redirect, url_for
from database.sqldb import get_db, close_db, init_db, insert_project

app = Flask(__name__)




@app.route('/')
def home():
    return render_template('home.html', active_page='home')


@app.route('/projects')
def projects():
    return render_template('projects.html', active_page='projects')


@app.route('/calendar')
def calendar():
    return render_template('calendar.html', active_page='calendar')


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
        print("Project Name:", project_name)
        print("Project Description:", project_description)
        if project_name:
            insert_project(project_name, project_description, project_poc, project_start_date, project_end_date)
            return redirect(url_for('project_detail', project_name=project_name))
    return render_template('new_project.html', active_page='projects')


@app.route('/project/<project_name>')
def project_detail(project_name):
    return render_template('project_detail.html', project_name=project_name, active_page='projects')


if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run(debug=True)