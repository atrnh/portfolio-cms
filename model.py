"""Data model."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.orm import exc
from sqlalchemy.inspection import inspect
from datetime import datetime
import json


db = SQLAlchemy()


class JSONMixin(object):
    """JSON helper mixins."""

    @staticmethod
    def get_json_from_list(instances,
                           make_js_list=False,
                           get_projects_object=None):
        """Return JSON of database instances."""

        if not make_js_list:
            if get_projects_object is not None:
                return json.dumps(
                    {inspect(instance).identity[0]:
                     json.loads(instance.get_attributes(get_projects_object))
                     for instance in instances}
                )
            return json.dumps(
                {inspect(instance).identity[0]:
                 json.loads(instance.get_attributes())
                 for instance in instances}
            )

        else:
            if get_projects_object is not None:
                return json.dumps(
                    [json.loads(instance.get_attributes(get_projects_object))
                     for instance in instances]
                )
            return json.dumps(
                [json.loads(instance.get_attributes())
                 for instance in instances]
            )

    def get_attributes(self, get_projects_object=True):
        """Get the attributes of an instance and their values.

        Does not include private attributes.
        """

        attributes = {}

        for attribute, value in self.__dict__.iteritems():
            if not attribute.startswith('_'):
                if type(value) is datetime:
                    attributes[attribute] = value.isoformat()
                elif isinstance(value, list):
                    try:
                        # We want a Python list instead of a JSON string since
                        # it will already get converted to JSON in
                        # return statement
                        if not isinstance(value[0], Project):
                            attributes[attribute] = json.loads(
                                self.get_json_from_list(value, True)
                            )
                        else:
                            if get_projects_object:
                                attributes[attribute] = json.loads(
                                    self.get_json_from_list(value)
                                )
                            else:
                                attributes[attribute] = json.loads(
                                    self.get_json_from_list(value, True)
                                )
                    except IndexError:
                        attributes[attribute] = []
                elif isinstance(value, db.Model):
                    attributes[attribute] = json.loads(value.get_attributes())
                else:
                    attributes[attribute] = value

        return json.dumps(attributes)


class Admin(db.Model):
    """A user who can login and access the admin dashboard."""

    __tablename__ = 'admins'

    email = db.Column(db.String(40), primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    hashed_password = db.Column(db.BigInteger)
    is_active = db.Column(db.Boolean)
    is_anonymous = db.Column(db.Boolean)
    is_authenticated = db.Column(db.Boolean)

    def __init__(self, email, first_name, last_name, hashed_password):
        """Instantiate an admin."""

        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.hashed_password = hashed_password
        self.is_active = True
        self.is_anonymous = False
        self.is_authenticated = True

    def __repr__(self):
        """Nice representation of Admin."""
        return '<Admin email={}'.format(self.email)

    def is_hashed_password(self, password):
        """Return true if stored password matches hash of given password."""

        return self.hashed_password == hash(password)

    def get_id(self):
        """Return unicode username."""

        return unicode(self.email)


class Config(db.Model):
    """Store user-defined configuration and settings."""

    __tablename__ = 'config'

    code = db.Column(db.String(80), primary_key=True)
    value = db.Column(db.String(100))

    def __init__(self, code, value):
        """Instantiate a config setting."""

        self.code = code
        self.value = value

    def __repr__(self):
        """Nice representation of Config."""

        return '<Config code={code} value={value}'.format(code=self.code,
                                                          value=self.value,
                                                          )


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
        """Nice representation of Category."""

        return '<Category id={id} title={title}>'.format(id=self.id,
                                                         title=self.title,
                                                         )


    @staticmethod
    def make_db_options(max_nest=0):
        if max_nest <= 0:
            return None
        elif max_nest == 1:
            return db.joinedload('projects')
        elif max_nest == 2:
            return (db.joinedload('projects')
                      .joinedload('media'))


    @classmethod
    def load_from_db(cls, max_nest=0, include_main_imgs=False):
        """Return categories with nested instances."""

        options = cls.make_db_options(max_nest)
        if include_main_imgs:
            options = options.joinedload('main_img')

        if max_nest:
            categories = cls.query.options(options).order_by(cls.id).all()
        else:
            categories = cls.query.order_by(cls.id).all()

        return categories


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

    def update(self, title=None, desc=None, category_id=None, tags=None,
               main_img_id=None):
        """Update a project's fields."""

        if title:
            self.title = title
        if desc:
            self.desc = desc
        if category_id:
            # Delete old CategoryProject
            try:
                db.session.delete(
                    CategoryProject.query.filter_by(
                        category_id=self.categories[0].id,
                        project_id=self.id).one()
                )
                db.session.commit()

                # Make new CategoryProject
                db.session.add(CategoryProject(category_id, self.id))
                db.session.commit()

            except exc.NoResultFound:
                # Make new CategoryProject
                db.session.add(CategoryProject(category_id, self.id))
                db.session.commit()

        if tags:
            project_tags = set([tag.code for tag in self.tags])
            # Filter out tags already in project_id
            filtered_tags = [tag for tag in tags
                             if tag not in
                             project_tags
                             ]
            # Make new tags
            tag_objects = Tag.create_tags(filtered_tags)
            db.session.add_all(tag_objects)
            db.session.commit()

            # make new associations
            db.session.add_all([TagProject(self.id, tag.code)
                                for tag in tag_objects
                                ])
            db.session.commit()

        if main_img_id:
            self.main_img_id = main_img_id

    def attach_tag(self, new_tag):
        """Attach new Tag to project."""

        project_tags = set([tag.code for tag in self.tags])
        print '\n\n\n\n\n\naaaaaaaa'
        print new_tag
        print '\n\n\n\n\n\n'

        if new_tag.code not in project_tags:
            db.session.add(TagProject(self.id, new_tag.code))
            db.session.commit()


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

    @classmethod
    def create_tags(cls, tags):
        """Take a list of strings that are tag codes and creates tags.

        Return a list of Tag objects.

        It only creates and commits tags if they do not already exist in the
        database.
        """

        # Get existing tags
        existing_tags = cls.query.filter(cls.code.in_(tags)).all()
        existing_tag_codes = set([e_tag.code for e_tag
                                  in existing_tags
                                  ])
        # Make new Tag objects if they do not exist
        new_tags = [
            cls(tag) for tag in tags
            if tag not in existing_tag_codes
        ]

        db.session.add_all(new_tags)
        db.session.commit()

        return existing_tags + new_tags


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

    projects = db.relationship('Project', secondary='projects_media')

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


class Page(db.Model, JSONMixin):
    """A page with html content."""

    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=True)

    def __init__(self, title, content=None):
        """Instantiate a Page."""

        self.title = title
        self.content = content

    def __repr__(self):
        """Nice represenation of a Page."""

        return '<Page id={id} title={title}>'.format(id=self.id,
                                                     title=self.title,
                                                     )


class ExternalLink(db.Model, JSONMixin):
    """An external link."""

    __tablename__ = 'external_links'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    url = db.Column(db.String(140))

    def __init__(self, title, url):
        """Instantiate an ExternalLink."""

        self.title = title
        self.url = url

    def __repr__(self):
        """Nice representation of an ExternalLink."""

        return '<ExternalLink id={id} title={title}'.format(id=self.id,
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
                'project_id={project_id}>').format(
            id=self.id,
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

    db.session.add_all(
        [Category('Test',
                  'This is a test category.'
                  ),
         Category('Sculptures',
                  'Another test category of wonderful sculptures.'
                  ),
         Category('Photos',
                  'Test another category of cool photos.'
                  ),
         ]
    )

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

    db.session.add_all([Config('title', 'My Portfolio')])

    db.session.commit()


def example_associations():
    """Create example associations for testing.

    ONLY call this after example_data or it will not work.
    """

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
