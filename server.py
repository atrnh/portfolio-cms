"""Server for Portfolio CMS."""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, Response, request, redirect)
from flask_debugtoolbar import DebugToolbarExtension
from model import (Category, Project, Tag, Media, Thumbnail, ProjectMedia,
                   CategoryProject, TagProject, db, connect_to_db,)
import json

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = 'ABC'

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def view_portfolio():
    """Portfolio homepage.

    Display all categories and their projects in the database.
    """

    categories = Category.query.options(db.joinedload('projects')
                                        ).order_by(Category.id
                                                   ).all()

    return render_template('portfolio.html', categories=categories)


@app.route('/categories.json')
def get_categories_json():
    """Return JSON list of all categories in database."""

    load_all = request.args.get('loadAll')

    if load_all:
        categories = Category.query.options(db.joinedload('projects')
                                              .joinedload('media')
                                            ).order_by(Category.id
                                                       ).all()
    else:
        categories = Category.query.options(db.joinedload('projects')
                                            ).order_by(Category.id
                                                       ).all()

    return Response(Category.get_json_from_list(categories),
                    mimetype='application/json'
                    )


@app.route('/category.json')
def get_category_json():
    """Return JSON category."""

    category_id = request.args.get('categoryId')

    category = Category.query.options(
        db.joinedload('projects')
    ).get(category_id)

    return Response(category.get_attributes(),
                    mimetype='application/json'
                    )


@app.route('/projects.json')
def get_category_projects_json():
    """Return JSON list of all projects.

    If categoryId is given in the request, return list of only projects
    associated with that category. If not, return list of all projects.
    """

    category_id = request.args.get('categoryId')

    if category_id:
        category_projects = Category.query.options(
            db.joinedload('projects')
        ).filter_by(id=category_id).one().projects

        return Response(Project.get_json_from_list(category_projects),
                        mimetype='application/json'
                        )
    else:
        projects = Project.query.all()

        return Response(Project.get_json_from_list(projects),
                        mimetype='application/json'
                        )


@app.route('/project.json')
def get_project_json():
    """Return JSON project."""

    project_id = request.args.get('projectId')

    project = Project.query.options(
        db.joinedload('media')
    ).get(project_id)

    return Response(project.get_attributes(),
                    mimetype='application/json'
                    )


@app.route('/admin/dashboard/')
def show_dashboard():
    """Admin dashboard.

    Display all categories, projects, and forms to create new ones.
    """

    categories = Category.query.options(db.joinedload('projects').
                                        joinedload('media')
                                        ).all()

    return render_template('dashboard.html', categories=categories)


@app.route('/admin/category', methods=['POST'])
def add_category():
    """Add a new category to the database."""

    title = request.args.get('categoryTitle')
    desc = request.args.get('categoryDesc')
    category = Category(title, desc)

    print title
    print desc

    db.session.add(category)
    db.session.commit()

    return redirect('/categories.json')


@app.route('/admin/project', methods=['POST'])
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
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
