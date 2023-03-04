"""Work model tests."""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Superheros, MySuperheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections 

os.environ['DATABASE_URL'] = "postgresql:///superhero-test"

from app import app

db.create_all()


class WorkModelTestCase(TestCase):
    """Test model for work."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        testuser = User.signup("John", "Smith", "test1", "password")
        self.testuser_id = 1111

        testuser.id = self.testuser_id
        db.session.commit()

        self.testuser = User.query.get(self.testuser_id)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_add_work_to_superheros(self):
        
        superheroinfo = SuperheroInfo(
            name="Batman"
        )

        work = Work(
            occupation="hero", 
            base_of_operation="NA")

        superheroinfo.work.append(work)
        self.testuser.superheros.append(superheroinfo)

        db.session.add(superheroinfo, work)
        db.session.commit()

        self.assertEqual(len(self.testuser.superheros), 1)
        self.assertEqual(self.testuser.superheros[0].name, "Batman")
        self.assertEqual(len(superheroinfo.work), 1)
        self.assertEqual(work.superheroinfo_id, superheroinfo.id)
        self.assertEqual(superheroinfo.work[0].occupation, "hero")
        self.assertEqual(superheroinfo.work[0].base_of_operation, "NA")

    def test_add_work_to_mysuperheros(self):
        
        superheroinfo = SuperheroInfo(
            name="Batman"
        )

        work = Work(
            occupation="hero", 
            base_of_operation="NA")

        superheroinfo.work.append(work)
        self.testuser.mysuperheros.append(superheroinfo)

        db.session.add(superheroinfo, work)
        db.session.commit()

        self.assertEqual(len(self.testuser.mysuperheros), 1)
        self.assertEqual(self.testuser.mysuperheros[0].name, "Batman")
        self.assertEqual(len(superheroinfo.work), 1)
        self.assertEqual(work.superheroinfo_id, superheroinfo.id)
        self.assertEqual(superheroinfo.work[0].occupation, "hero")
        self.assertEqual(superheroinfo.work[0].base_of_operation, "NA")