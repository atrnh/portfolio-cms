"""Server for Portfolio CMS."""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, jsonify)
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

    return jsonify(Category.get_json_from_list(categories, 'category'))


if __name__ == '__main__':
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
