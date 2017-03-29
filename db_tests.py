import unittest
from server import app
from model import (Category, Project, Tag, Media, Thumbnail, ProjectMedia,
                   CategoryProject, TagProject, db, connect_to_db,
                   example_data,)

class FlaskTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Set up."""

        connect_to_db(app, 'postgresql:///testdb')

        db.create_all()
        example_data()

    def tearDown(self):
        """Tear down."""

        db.session.close()
        db.drop_all()

    def testCategoryProject(self):
        """Test categories_projects table."""

        c = Category.query.get(1)
        p = Project.query.get(1)

        db.session.add(CategoryProject(c.id, p.id))
        db.session.commit()

        cp = CategoryProject.query.get(1)

        self.assertIsInstance(cp, CategoryProject)
        self.assertIs(c.projects[0], p)
        self.assertIs(p.categories[0], c)


if __name__ == "__main__":
    unittest.main()
