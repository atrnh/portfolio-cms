"""Server for Portfolio CMS."""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, Response, request, redirect)
from flask_debugtoolbar import DebugToolbarExtension
from flask_uploads import UploadSet, IMAGES, configure_uploads
import json
from model import (Category, Project, Tag, Media, ProjectMedia,
                   CategoryProject, TagProject, db, connect_to_db,
                   Admin,
                   )
from flask_login import LoginManager, login_user, login_required


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = 'ABC'

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

# Configuration for uploading images
app.config['UPLOADS_DEFAULT_DEST'] = 'static'
images = UploadSet('images', IMAGES)
configure_uploads(app, (images,))

# Configuration for login handling
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(email):
    """Requirement for flask_login."""

    return Admin.query.get(email)


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
def get_categories_json(load_all=False):
    """Return JSON list of all categories in database.

    If loadAll is present, greedily load all nested objects.
    """

    if not load_all:
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
def get_category_json(category_id=None):
    """Return JSON category."""

    if not category_id:
        category_id = request.args.get('categoryId')

    category = Category.query.options(
        db.joinedload('projects')
          .joinedload('main_img')
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

        return jsonify_list(
            Project.get_json_from_list(category_projects)
        )

    else:
        projects = Project.query.all()

        return jsonify_list(Project.get_json_from_list(projects))


@app.route('/project.json')
def get_project_json(project_id=None):
    """Return JSON project."""

    if not project_id:
        project_id = request.args.get('projectId')

    project = Project.query.options(
        db.joinedload('categories'),
        db.joinedload('media'),
        db.joinedload('tags')
    ).get(project_id)

    return jsonify_list(project.get_attributes())


@app.route('/media.json')
def get_media_json(media_id=None):
    """Return JSON media."""

    if not media_id:
        media_id = request.args.get('mediaId')

    media = Media.query.get(media_id)

    return jsonify_list(media.get_attributes())


@app.route('/tags.json')
def get_tags_json():
    """Return JSON array of all Tag objects."""

    tags = Tag.query.all()

    return jsonify_list(Tag.get_json_from_list(tags))


@app.route('/tag.json')
def get_tag_json(tag_code=None):
    """Return JSON for a Tag."""

    if not tag_code:
        tag_code = request.args.get('tagCode')

    tag = Tag.query.options(
        db.joinedload('projects')
          .joinedload('main_img')
    ).get(tag_code)

    return jsonify_list(tag.get_attributes())


@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    """Display log in form and handle logging in user."""

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        admin = Admin.query.get(email)

        if admin.is_hashed_password(password):
            admin.is_authenticated = True
            login_user(admin)

            return redirect('/admin/dashboard')

    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    """Register a user."""

    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')

    db.session.add(Admin(email, first_name, last_name, hash(password)))
    db.session.commit()

    return redirect('/admin/login')


@app.route('/admin/dashboard/')
@login_required
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

    return get_category_json(category.id)


@app.route('/admin/category/<category_id>', methods=['DELETE', 'POST'])
def update_category(category_id):
    """Delete or update a category from the database."""

    if request.method == 'DELETE':
        deleted = get_category_json(category_id)
        db.session.delete(Category.query.get(category_id))
        db.session.commit()

        return deleted

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

        return get_category_json(category_id)


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
    if tags:
        all_tags = Tag.create_tags(tags)
        db.session.add_all([TagProject(project.id, tag.code)
                            for tag in all_tags
                            ])
        db.session.commit()

    return get_project_json(project.id)


@app.route('/admin/project/<project_id>', methods=['DELETE', 'POST'])
def update_project(project_id):
    """Delete or update a project from the database."""

    project = Project.query.get(project_id)

    if request.method == 'DELETE':
        db.session.delete(project)
        db.session.commit()

        return get_categories_json(True)

    elif request.method == 'POST':
        data = json.loads(request.data.decode())

        title = data.get('title')
        desc = data.get('desc')
        category_id = data.get('categoryId')
        tags = data.get('tags')
        main_img_id = data.get('mainImgId')

        project.update(title, desc, category_id, tags, main_img_id)

        db.session.commit()

        return get_project_json(project_id)


@app.route('/admin/project/<project_id>/new_tag', methods=['POST'])
def tag_project(project_id):
    """Attach a tag to project."""

    # import pdb; pdb.set_trace()

    data = json.loads(request.data.decode())
    tag_code = data.get('code')
    project = Project.query.get(project_id)
    tag = Tag.query.get(tag_code)

    if tag:
        project.attach_tag(tag)

        return jsonify_list(tag.get_attributes())

    else:
        tag = Tag(tag_code)
        db.session.add(tag)
        db.session.commit()

        project.attach_tag(tag)

        return jsonify_list(tag.get_attributes())


@app.route('/admin/project/<project_id>/tag/<tag_code>',
           methods=['DELETE']
           )
def delete_project_tag(project_id, tag_code):
    """Delete a tag from a project."""

    db.session.delete(TagProject.query.filter_by(project_id=project_id,
                                                 tag_code=tag_code
                                                 ).one())
    db.session.commit()

    # Delete tag if it has no associated projects
    tag = Tag.query.get(tag_code)
    if not tag.projects:
        db.session.delete(tag)
        db.session.commit()

    return get_project_json(project_id)


@app.route('/upload', methods=['POST'])
def upload():
    """Handle uploading new images."""

    filename = images.save(request.files['imageFile'])

    project_id = request.form.get('projectId')

    media = Media('test', images.path(filename))
    db.session.add(media)
    db.session.commit()

    project_media = ProjectMedia(project_id, media.id)
    db.session.add(project_media)
    db.session.commit()

    return get_media_json(media.id)


@app.route('/admin/project/<project_id>/media/<media_id>', methods=['POST', 'DELETE'])
def update_media(project_id, media_id):
    """Update or delete media."""

    media = Media.query.get(media_id)

    if request.method == 'POST':
        data = json.loads(request.data.decode())

        title = data.get('title')
        desc = data.get('desc')

        if title:
            media.title = title
            db.session.commit()
        if desc:
            media.desc = desc
            db.session.commit()

        return jsonify_list(media.get_attributes())

    elif request.method == 'DELETE':
        project_media = ProjectMedia.query.filter_by(project_id=project_id,
                                                     media_id=media_id
                                                     ).one()
        db.session.delete(project_media)
        db.session.commit()

        db.session.delete(media)
        db.session.commit()

        return get_project_json(project_id)


def jsonify_list(objects):
    """Return a Response object with a top-level array of objects."""

    return Response(objects, mimetype='application/json')


if __name__ == '__main__':
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
