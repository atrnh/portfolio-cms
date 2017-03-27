"""Data model for Portfolio CMS."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Category(db.Model):
    """A category."""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    desc = db.Column(db.String(500), nullable=True)

    projects = db.relationship('Project', secondary='categories_projects')

    def __init__(self, title, desc=None):
        """Instantiate a Category."""

        self.title = title
        self.desc = desc

    def __repr__(self):
        """Nice represenation of Category."""

        return '<Category id={id} title={title}'.format(self.id, self.title)


class Project(db.Model):
    """A project."""

    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    desc = db.Column(db.String(500), nullable=True)
    date_created = db.Column(db.Date, nullable=True)
    date_updated = db.Column(db.DateTime)

    main_img = db.Column(db.ForeignKey('media.id'))
    categories = db.relationship('Category', secondary='categories_projects')

    def __init__(self, title, desc=None, date_created=None):
        """Instantiate a Project."""

        self.title = title
        self.desc = desc
        self.date_created = date_created
        self.date_updated = datetime.now()

    def __repr__(self):
        """Nice representation of Project."""

        return '<Project id={id} title={title}'.format(self.id, self.title)


class Tag(db.Model):
    """A tag."""

    __tablename__ = 'tags'

    code = db.Column(db.String(50), primary_key=True)

    def __init__(self, code):
        """Instantiate a Tag."""

        self.code = code

    def __repr__(self):
        """Nice representation of a Tag."""

        return '<Tag code={}'.format(self.code)


class CategoryProject(db.Model):
    """An association between a Category and Project."""

    __tablename__ = 'categories_projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.ForeignKey('categories.id'))
    project_id = db.Column(db.ForeignKey('projects.id'))

    def __init__(self, category_id, project_id):
        """Instantiate a CategoryProject."""

        self.category_id = category_id
        self.project_id = project_id

    def __repr__(self):
        """Nice representation of a CategoryProject."""

        return ('<CategoryProject id={id} category_id={category_id}' +
                'project_id={project_id}>').format(self.id,
                                                   self.category_id,
                                                   self.project_id)


class TagProject(db.Model):
    """An association between a Tag and Project."""

    pass


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///kanban'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
