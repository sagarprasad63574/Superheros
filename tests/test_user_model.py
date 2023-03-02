"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Superheros, MySuperheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections 

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///superhero-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        user1 = User.signup("John", "Simth", "test1", "password")
        user_id_1 = 1111
        user1.id = user_id_1

        user2 = User.signup("Bill", "Simth", "test2", "password")
        user_id_2 = 2222
        user2.id = user_id_2

        db.session.commit()

        user1 = User.query.get(user_id_1)
        user2 = User.query.get(user_id_2)

        self.user1 = user1
        self.user_id_1 = user_id_1

        self.user2 = user2
        self.user_id_2 = user_id_2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            first_name = "Cody",
            last_name = "Smith",
            username="test3",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no favorties and my-superheros
        self.assertEqual(len(u.superheros), 0)
        self.assertEqual(len(u.mysuperheros), 0)

    def test_user_favorite_superheros(self):
        superhero = SuperheroInfo(name="Batman")

        self.user1.superheros.append(superhero)
        db.session.commit()

        self.assertEqual(len(self.user1.superheros), 1)

        self.assertEqual(self.user1.superheros[0].id, superhero.id)

    def test_user_mysuperheros(self):
        mysuperhero = SuperheroInfo(name="New Superhero")

        self.user1.mysuperheros.append(mysuperhero)
        db.session.commit()

        self.assertEqual(len(self.user1.mysuperheros), 1)

        self.assertEqual(self.user1.mysuperheros[0].id, mysuperhero.id)

    def test_valid_signup(self):
        user_test = User.signup("Bob", "Smith", "test3", "password")
        user_id = 3333
        user_test.id = user_id
        db.session.commit()

        user_test = User.query.get(user_id)
        self.assertIsNotNone(user_test)
        self.assertEqual(user_test.first_name, "Bob")
        self.assertEqual(user_test.last_name, "Smith")
        self.assertEqual(user_test.username, "test3")
        self.assertNotEqual(user_test.password, "password")
        self.assertTrue(user_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        user_test = User.signup("Ken", "Davis", None, "password")
        user_id = 4444
        user_test.id = user_id
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("John", "Davis", "test3", "")
        
        with self.assertRaises(ValueError) as context:
            User.signup("Lady", "Smith", "test4", None)

    def test_valid_authentication(self):
        user = User.authenticate(self.user1.username, "password")
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.user_id_1)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.user1.username, "badpassword"))