"""Appearance model tests."""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Superheros, MySuperheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections 

os.environ['DATABASE_URL'] = "postgresql:///superhero-test"

from app import app

db.create_all()


class AppearanceModelTestCase(TestCase):
    """Test model for appearance."""

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

    def test_add_appearance_to_superheros(self):
        
        superheroinfo = SuperheroInfo(
            name="Batman"
        )

        appearance = Appearance(
            gender="Male", 
            race="White", 
            height="5'9", 
            weight="120lb", 
            eye_color="Black",
            hair_color="Black")

        superheroinfo.appearance.append(appearance)
        self.testuser.superheros.append(superheroinfo)

        db.session.add(superheroinfo, appearance)
        db.session.commit()

        self.assertEqual(len(self.testuser.superheros), 1)
        self.assertEqual(self.testuser.superheros[0].name, "Batman")
        self.assertEqual(len(superheroinfo.appearance), 1)
        self.assertEqual(appearance.superheroinfo_id, superheroinfo.id)
        self.assertEqual(superheroinfo.appearance[0].gender, "Male")
        self.assertEqual(superheroinfo.appearance[0].race, "White")
        self.assertEqual(superheroinfo.appearance[0].height, "5'9")
        self.assertEqual(superheroinfo.appearance[0].weight, "120lb")
        self.assertEqual(superheroinfo.appearance[0].eye_color, "Black")        
        self.assertEqual(superheroinfo.appearance[0].hair_color, "Black")
    
    def test_add_appearance_to_mysuperheros(self):
        
        superheroinfo = SuperheroInfo(
            name="Batman"
        )

        appearance = Appearance(
            gender="Male", 
            race="White", 
            height="5'9", 
            weight="120lb", 
            eye_color="Black",
            hair_color="Black")

        superheroinfo.appearance.append(appearance)
        self.testuser.mysuperheros.append(superheroinfo)

        db.session.add(superheroinfo, appearance)
        db.session.commit()

        self.assertEqual(len(self.testuser.mysuperheros), 1)
        self.assertEqual(self.testuser.mysuperheros[0].name, "Batman")
        self.assertEqual(len(superheroinfo.appearance), 1)
        self.assertEqual(appearance.superheroinfo_id, superheroinfo.id)
        self.assertEqual(superheroinfo.appearance[0].gender, "Male")
        self.assertEqual(superheroinfo.appearance[0].race, "White")
        self.assertEqual(superheroinfo.appearance[0].height, "5'9")
        self.assertEqual(superheroinfo.appearance[0].weight, "120lb")
        self.assertEqual(superheroinfo.appearance[0].eye_color, "Black")        
        self.assertEqual(superheroinfo.appearance[0].hair_color, "Black")