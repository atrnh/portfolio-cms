"""Server for Portfolio CMS."""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, Response, request, redirect)
from flask_debugtoolbar import DebugToolbarExtension
from model import (Category, Project, Tag, Media, Thumbnail, ProjectMedia,
                   CategoryProject, TagProject, db, connect_to_db,)

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = 'ABC'

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage.

    Display all categories and their projects in the database.
    """

    categories = Category.query.options(db.joinedload('projects')
                                        ).all()

    return render_template('index.html', categories=categories)


@app.route('/categories.json')
def get_categories_json():

    categories = Category.query.options(db.joinedload('projects')
                                        ).all()

    return Response(Category.get_json_from_list(categories),
                    mimetype='application/json'
                    )


@app.route('/category/<category_id>/projects.json')
def get_category_projects_json(category_id):

    projects = Category.query.options(
        db.joinedload('projects')
    ).filter_by(id=category_id).one().projects

    print projects

    return Response(Project.get_json_from_list(projects),
                    mimetype='application/json'
                    )


@app.route('/admin/dashboard')
def show_dashboard():
    """Admin dashboard.

    Display all categories, projects, and forms to create new ones.
    """

    categories = Category.query.options(db.joinedload('projects')
                                        ).all()

    return render_template('dashboard.html', categories=categories)


@app.route('/new_category', methods=['POST'])
def add_category():
    """Add a new category to the database."""

    title = request.form.get('title')
    desc = request.form.get('desc')
    category = Category(title, desc)

    db.session.add(category)
    db.session.commit()

    return redirect('/admin/dashboard')


@app.route('/new_project', methods=['POST'])
def add_project():
    """Add a new project to the database."""

    title = request.form.get('title')
    desc = request.form.get('desc')
    category_id = request.form.get('category_id')

    project = Project(title, desc=desc)

    db.session.add(project)
    db.session.commit()

    db.session.add(CategoryProject(category_id, project.id))
    db.session.commit()

    return redirect('/admin/dashboard')


if __name__ == '__main__':
    app.debug = False
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
