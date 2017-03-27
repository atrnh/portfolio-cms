"""Data model for Portfolio CMS."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Category(db.Model):
    """A category."""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    desc = db.Column(db.Text, nullable=True)

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
    desc = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.Date, nullable=True)
    date_updated = db.Column(db.DateTime)

    main_img_id = db.Column(db.ForeignKey('media.id'))
    main_img = db.relationship('Media')

    categories = db.relationship('Category', secondary='categories_projects')
    tags = db.relationship('Tag', secondary='tags_projects')
    media = db.relationship('Media', secondary='projects_media')

    def __init__(self, title, main_img_id, desc=None, date_created=None):
        """Instantiate a Project."""

        self.title = title
        self.desc = desc
        self.date_created = date_created
        self.date_updated = datetime.now()
        self.main_img_id = main_img_id

    def __repr__(self):
        """Nice representation of Project."""

        return '<Project id={id} title={title}'.format(self.id, self.title)


class Tag(db.Model):
    """A tag."""

    __tablename__ = 'tags'

    code = db.Column(db.String(50), primary_key=True)

    projects = db.relationship('Project', secondary='tags_projects')

    def __init__(self, code):
        """Instantiate a Tag."""

        self.code = code

    def __repr__(self):
        """Nice representation of a Tag."""

        return '<Tag code={}'.format(self.code)


class Media(db.Model):
    """An image or embedded video."""

    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    desc = db.Column(db.Text, nullable=True)
    date_updated = db.Column(db.DateTime)
    source_url = db.Column(db.String(70))

    def __init__(self, title, source_url, desc=None):
        """Instantiate a Media."""

        self.title = title
        self.source_url = source_url
        self.desc = desc
        self.date_updated = datetime.now()


class Thumbnail(db.Model):
    pass


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

        return ('<CategoryProject id={id} category_id={category_id} ' +
                'project_id={project_id}>').format(id=self.id,
                                                   category_id=self.category_id,
                                                   project_id=self.project_id,
                                                   )


class TagProject(db.Model):
    """An association between a Tag and Project."""

    __tablename__ = 'tags_projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.ForeignKey('projects.id'))
    tag_code = db.Column(db.ForeignKey('tags.code'))

    def __init__(self, project_id, tag_code):
        """Instantiate a TagProject."""

        self.project_id = project_id
        self.tag_code = tag_code

    def __repr__(self):
        """Nice representation of a TagProject."""

        return ('<TagProject id={id} project_id={project_id} ' +
                'tag_code={tag_code}').format(id=self.id,
                                              project_id=self.project_id,
                                              tag_code=self.tag_code,
                                              )


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
