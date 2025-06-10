from flask import Flask, render_template, request, redirect, url_for

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
            return redirect(url_for('project_detail', project_name=project_name))
    return render_template('new_project.html', active_page='projects')


@app.route('/project/<project_name>')
def project_detail(project_name):
    return render_template('project_detail.html', project_name=project_name, active_page='projects')


if __name__ == '__main__':
    app.run(debug=True)