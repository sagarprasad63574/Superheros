"""Biography model tests."""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Superheros, MySuperheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections 

os.environ['DATABASE_URL'] = "postgresql:///superhero-test"

from app import app

db.create_all()


class BiographyModelTestCase(TestCase):
    """Test model for biography."""

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

    def test_add_biography_to_superheros(self):
        
        superheroinfo = SuperheroInfo(
            name="Batman"
        )

        biography = Biography(
            full_name="Batman 1", 
            place_of_birth="NY", 
            first_appearance="Maine", 
            alter_egos="No alter egos", 
            publisher="DC")

        superheroinfo.biography.append(biography)
        self.testuser.superheros.append(superheroinfo)

        db.session.add(superheroinfo, biography)
        db.session.commit()

        self.assertEqual(len(self.testuser.superheros), 1)
        self.assertEqual(self.testuser.superheros[0].name, "Batman")
        self.assertEqual(len(superheroinfo.biography), 1)
        self.assertEqual(biography.superheroinfo_id, superheroinfo.id)
        self.assertEqual(superheroinfo.biography[0].full_name, "Batman 1")
        self.assertEqual(superheroinfo.biography[0].place_of_birth, "NY")
        self.assertEqual(superheroinfo.biography[0].first_appearance, "Maine")
        self.assertEqual(superheroinfo.biography[0].alter_egos, "No alter egos")
        self.assertEqual(superheroinfo.biography[0].publisher, "DC")
    
    def test_add_biography_to_mysuperheros(self):
        
        superheroinfo = SuperheroInfo(
            name="Batman"
        )

        biography = Biography(
            full_name="Batman 1", 
            place_of_birth="NY", 
            first_appearance="Maine", 
            alter_egos="No alter egos", 
            publisher="DC")

        superheroinfo.biography.append(biography)
        self.testuser.mysuperheros.append(superheroinfo)

        db.session.add(superheroinfo, biography)
        db.session.commit()

        self.assertEqual(len(self.testuser.mysuperheros), 1)
        self.assertEqual(self.testuser.mysuperheros[0].name, "Batman")
        self.assertEqual(len(superheroinfo.biography), 1)
        self.assertEqual(biography.superheroinfo_id, superheroinfo.id)
        self.assertEqual(superheroinfo.biography[0].full_name, "Batman 1")
        self.assertEqual(superheroinfo.biography[0].place_of_birth, "NY")
        self.assertEqual(superheroinfo.biography[0].first_appearance, "Maine")
        self.assertEqual(superheroinfo.biography[0].alter_egos, "No alter egos")
        self.assertEqual(superheroinfo.biography[0].publisher, "DC")