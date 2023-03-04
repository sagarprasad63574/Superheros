"""Login/Sign Up view tests."""

import os
from unittest import TestCase

from models import db, connect_db, User, Superheros, MySuperheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections 

os.environ['DATABASE_URL'] = "postgresql:///superhero-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for sign up/login."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.user1 = User.signup("John", "Smith", "testing1", "password")
        self.user1_id = 1111
        self.user1.id = self.user1_id

        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_index(self):
        with self.client as c:
            res = c.get("/")

            self.assertIn("Welcome to my Superhero List", str(res.data))

    def test_user_logged_in(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.get("/", follow_redirects=True)

            self.assertIn("Search For Superhero", str(res.data))

    def test_login_user(self):
        with self.client as c:
            res = c.post("/login", data={"username": "testing1", "password": "password"}, follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Search For Superhero", str(res.data))

    def test_invaild_login_user(self):
        with self.client as c:
            res = c.post("/login", data={"username": "testing6", "password": "password"})

            self.assertEqual(res.status_code, 200)
            self.assertIn("Invalid credentials.", str(res.data))

    def test_signup_user(self):
        with self.client as c:
            res = c.post("/signup", data={"first_name": "Poppy", "last_name": "Smith", "username": "testing6", 
            "password": "password"}, follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Search For Superhero", str(res.data))

    def test_logout_user(self):
        with self.client as c:
            res = c.post("/login", data={"username": "testing1", "password": "password"}, follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Search For Superhero", str(res.data))

            res = c.get("/logout", follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Logged out", str(res.data))