from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.inspection import inspect
import json

db = SQLAlchemy()


# class DBMixin(object):
#     """Database helper mixins."""
#
#     pass


class JSONMixin(object):
    """JSON helper mixins."""

    @staticmethod
    def get_json_from_list(instances):
        """Return JSON of a list of instances."""

        return json.dumps(
            [instance.get_attributes() for instance in instances]
        )

    def get_attributes(self):
        """Get the attributes of an instance and their values.

        Does not include private attributes or attributes containing database
        objects.
        """

        attributes = {}

        for attribute, value in self.__dict__.iteritems():
            if not attribute.startswith('_'):
                if type(value) is datetime:
                    attributes[attribute] = value.isoformat()
                elif isinstance(value, list):
                    try:
                        attributes[attribute] = self.get_json_from_list(
                            value
                        )
                    except IndexError:
                        attributes[attribute] = []
                else:
                    attributes[attribute] = value

        return attributes


class Category(db.Model, JSONMixin):
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

        return '<Category id={id} title={title}>'.format(id=self.id,
                                                         title=self.title,
                                                         )


class Project(db.Model, JSONMixin):
    """A project."""

    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    desc = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.Date, nullable=True)
    date_updated = db.Column(db.DateTime(timezone=True),
                             server_default=func.now(),
                             onupdate=func.now(),
                             )

    main_img_id = db.Column(db.Integer,
                            db.ForeignKey('media.id'),
                            nullable=True,
                            )
    main_img = db.relationship('Media')

    categories = db.relationship('Category', secondary='categories_projects')
    tags = db.relationship('Tag', secondary='tags_projects')
    media = db.relationship('Media', secondary='projects_media')

    def __init__(self, title, main_img_id=None, desc=None, date_created=None):
        """Instantiate a Project."""

        self.title = title
        self.desc = desc
        self.date_created = date_created
        self.main_img_id = main_img_id

    def __repr__(self):
        """Nice representation of Project."""

        return '<Project id={id} title={title}>'.format(id=self.id,
                                                        title=self.title,
                                                        )


class Tag(db.Model, JSONMixin):
    """A tag."""

    __tablename__ = 'tags'

    code = db.Column(db.String(50), primary_key=True)

    projects = db.relationship('Project', secondary='tags_projects')

    def __init__(self, code):
        """Instantiate a Tag."""

        self.code = code

    def __repr__(self):
        """Nice representation of a Tag."""

        return '<Tag code={}>'.format(self.code)


class Media(db.Model, JSONMixin):
    """An image or embedded video."""

    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    desc = db.Column(db.Text, nullable=True)
    date_updated = db.Column(db.DateTime(timezone=True),
                             server_default=func.now(),
                             onupdate=func.now(),
                             )
    source_url = db.Column(db.String(70))
    thumbnail_id = db.Column(db.Integer,
                             db.ForeignKey('thumbnails.id'),
                             nullable=True,
                             )

    thumbnail = db.relationship('Thumbnail')

    projects = db.relationship('Media', secondary='projects_media')

    def __init__(self, title, source_url, desc=None):
        """Instantiate a Media."""

        self.title = title
        self.source_url = source_url
        self.desc = desc

    def __repr__(self):
        """Nice representation of a Media."""

        return '<Media id={id} title={title}>'.format(id=self.id,
                                                      title=self.title,
                                                      )


class Thumbnail(db.Model):
    """A thumbnail."""

    __tablename__ = 'thumbnails'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_url = db.Column(db.String(70))

    def __init__(self, source_url):
        """Instantiate a Thumbnail."""

        self.source_url = source_url

    def __repr__(self):
        """Nice represenation of a Thumbnail."""

        return '<Thumbnail id={id}>'.format(id=self.id)


class ProjectMedia(db.Model):
    """An association between a Project and Media."""

    __tablename__ = 'projects_media'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'))

    def __init__(self, project_id, media_id):
        """Instantiate a ProjectMedia."""

        self.project_id = project_id
        self.media_id = media_id

    def __repr__(self):
        """Nice representation of a ProjectMedia."""

        return ('<ProjectMedia id={id} project_id={project_id} ' +
                'media_id={media_id}>').format(id=self.id,
                                               project_id=self.project_id,
                                               media_id=self.media_id,
                                               )


class CategoryProject(db.Model):
    """An association between a Category and Project."""

    __tablename__ = 'categories_projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

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
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    tag_code = db.Column(db.String(50), db.ForeignKey('tags.code'))

    def __init__(self, project_id, tag_code):
        """Instantiate a TagProject."""

        self.project_id = project_id
        self.tag_code = tag_code

    def __repr__(self):
        """Nice representation of a TagProject."""

        return ('<TagProject id={id} project_id={project_id} ' +
                'tag_code={tag_code}>').format(id=self.id,
                                               project_id=self.project_id,
                                               tag_code=self.tag_code,
                                               )


##############################################################################
# Helper functions

def connect_to_db(app, db_uri='postgresql:///portfolio'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def example_data():
    """Create example data for testing."""

    db.session.add_all([Category('Test',
                                 'This is a test category.'),
                        Category('Sculptures',
                                 'Another test category of wonderful sculptures.'),
                        Category('Photos',
                                 'Test another category of cool photos.'),
                        ])

    db.session.add_all([Media('Test Image',
                              'test.jpg',
                              'This is a test image.'),
                        Media('Test Cat',
                              'cat.jpg',
                              'Test image of a cat.'),
                        Media('Test Sculpture',
                              'sculpture.jpg',
                              'A test sculpture.'),
                        Media('Cool Test',
                              'cool.jpg',
                              'Another fake, test image.'),
                        ])

    db.session.add_all([Project('Test Project',
                                desc='This is a test project.'),
                        Project('Cool Cats',
                                desc='Test project about cool cats.'),
                        Project('Cool Dogs',
                                desc='Test project about cool dogs.'),
                        ])

    db.session.add_all([Tag('test-tag'),
                        Tag('animals'),
                        ])

    db.session.add_all([Thumbnail('test_thumb.jpg'),
                        Thumbnail('cat_thumb.jpg'),
                        Thumbnail('sculpture_thumb.jpg'),
                        Thumbnail('cool_thumb.jpg'),
                        ])

    db.session.commit()


def example_associations():
    """Create example associations for testing.

    ONLY call this after example_data or it will not work."""

    categories = Category.query.all()
    projects = Project.query.all()

    db.session.add_all([CategoryProject(categories[0].id,
                                        projects[0].id),
                        CategoryProject(categories[2].id,
                                        projects[1].id),
                        CategoryProject(categories[2].id,
                                        projects[2].id),
                        ])
    db.session.commit()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
