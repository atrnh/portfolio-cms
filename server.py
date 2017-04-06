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
    """Return JSON list of all categories in database.

    If loadAll is present, greedily load all nested objects.
    """

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

    return jsonify_list(Category.get_json_from_list(categories))


@app.route('/category.json')
def get_category_json():
    """Return JSON category."""

    category_id = request.args.get('categoryId')

    category = Category.query.options(
        db.joinedload('projects')
    ).get(category_id)

    return jsonify_list(category.get_attributes())


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

        return jsonify_list(Project.get_json_from_list(projects))


@app.route('/project.json')
def get_project_json():
    """Return JSON project."""

    project_id = request.args.get('projectId')

    project = Project.query.options(
        db.joinedload('categories'),
        db.joinedload('media'),
        db.joinedload('tags')
    ).get(project_id)

    return jsonify_list(project.get_attributes())


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

    data = json.loads(request.data.decode())

    title = data.get('title')
    desc = data.get('desc')
    category = Category(title, desc)

    db.session.add(category)
    db.session.commit()

    return redirect('/categories.json')


@app.route('/admin/category/<category_id>', methods=['DELETE', 'POST'])
def update_category(category_id):
    """Delete or update a category from the database."""

    if request.method == 'DELETE':
        db.session.delete(Category.query.get(category_id))
        db.session.commit()

        categories = Category.query.options(db.joinedload('projects')
                                              .joinedload('media')
                                            ).order_by(Category.id
                                                       ).all()

        return jsonify_list(Category.get_json_from_list(categories))

    elif request.method == 'POST':
        data = json.loads(request.data.decode())

        title = data.get('title')
        desc = data.get('desc')

        category = Category.query.get(category_id)

        if title:
            category.title = title

        if desc:
            category.desc = desc

        db.session.commit()

        categories = Category.query.options(db.joinedload('projects')
                                              .joinedload('media')
                                            ).order_by(Category.id
                                                       ).all()

        return jsonify_list(Category.get_json_from_list(categories))


@app.route('/admin/project', methods=['POST'])
def add_project():
    """Add a new project to the database."""

    data = json.loads(request.data.decode())

    title = data.get('title')
    desc = data.get('desc')
    category_id = data.get('categoryId')
    tags = data.get('tags')

    # Add project
    project = Project(title, desc=desc)
    db.session.add(project)
    db.session.commit()

    # Add association
    db.session.add(CategoryProject(category_id, project.id))
    db.session.commit()

    # Add tags
    all_tags = Tag.create_tags(tags)
    db.session.add_all([TagProject(project.id, tag.code)
                        for tag in all_tags
                        ])
    db.session.commit()

    return redirect('/admin/dashboard')


@app.route('/admin/project/<project_id>', methods=['DELETE', 'POST'])
def update_project(project_id):
    """Delete or update a project from the database."""

    if request.method == 'DELETE':
        db.session.delete(Project.query.get(project_id))
        db.session.commit()

        categories = Category.query.options(db.joinedload('projects')
                                              .joinedload('media')
                                            ).order_by(Category.id
                                                       ).all()

        return jsonify_list(Category.get_json_from_list(categories))

    elif request.method == 'POST':
        data = json.loads(request.data.decode())

        title = data.get('title')
        desc = data.get('desc')
        category_id = data.get('categoryId')
        tags = data.get('tags')

        project = Project.query.get(project_id)
        original_cat = project.categories[0]

        if title:
            project.title = title
        if desc:
            project.desc = desc
        if category_id:
            # Delete old CategoryProject
            db.session.delete(
                CategoryProject.query.filter_by(category_id=original_cat.id,
                                                project_id=project_id).one()
            )
            db.session.commit()

            # Make new CategoryProject
            db.session.add(CategoryProject(category_id, project_id))
            db.session.commit()

        db.session.commit()

        categories = Category.query.options(db.joinedload('projects')
                                              .joinedload('media')
                                            ).order_by(Category.id
                                                       ).all()

        return jsonify_list(Category.get_json_from_list(categories))


def jsonify_list(objects):
    """Return a Response object with a top-level array of objects."""

    return Response(objects, mimetype='application/json')


if __name__ == '__main__':
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
