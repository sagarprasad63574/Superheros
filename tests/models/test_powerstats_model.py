"""Powerstats model tests."""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Superheros, MySuperheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections 

os.environ['DATABASE_URL'] = "postgresql:///superhero-test"

from app import app

db.create_all()


class PowerstatsModelTestCase(TestCase):
    """Test model for powerstats."""

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

    def test_add_powerstats_to_superheros(self):
        
        superheroinfo = SuperheroInfo(
            name="Batman"
        )

        powerstats = Powerstats(
            intelligence="10", 
            strength="20", 
            speed="30", 
            durability="40", 
            power="50", 
            combat="60")

        superheroinfo.powerstats.append(powerstats)
        self.testuser.superheros.append(superheroinfo)

        db.session.add(superheroinfo, powerstats)
        db.session.commit()

        self.assertEqual(len(self.testuser.superheros), 1)
        self.assertEqual(self.testuser.superheros[0].name, "Batman")
        self.assertEqual(len(superheroinfo.powerstats), 1)
        self.assertEqual(powerstats.superheroinfo_id, superheroinfo.id)
        self.assertEqual(superheroinfo.powerstats[0].intelligence, "10")
        self.assertEqual(superheroinfo.powerstats[0].strength, "20")
        self.assertEqual(superheroinfo.powerstats[0].speed, "30")
        self.assertEqual(superheroinfo.powerstats[0].durability, "40")
        self.assertEqual(superheroinfo.powerstats[0].power, "50")
        self.assertEqual(superheroinfo.powerstats[0].combat, "60")

    def test_powerstats_model(self):
        
        superheroinfo = SuperheroInfo(
            name="Batman"
        )

        powerstats = Powerstats(
            intelligence="10", 
            strength="20", 
            speed="30", 
            durability="40", 
            power="50", 
            combat="60")

        superheroinfo.powerstats.append(powerstats)
        self.testuser.mysuperheros.append(superheroinfo)

        db.session.add(superheroinfo, powerstats)
        db.session.commit()

        self.assertEqual(len(self.testuser.mysuperheros), 1)
        self.assertEqual(self.testuser.mysuperheros[0].name, "Batman")
        self.assertEqual(len(superheroinfo.powerstats), 1)
        self.assertEqual(powerstats.superheroinfo_id, superheroinfo.id)
        self.assertEqual(superheroinfo.powerstats[0].intelligence, "10")
        self.assertEqual(superheroinfo.powerstats[0].strength, "20")
        self.assertEqual(superheroinfo.powerstats[0].speed, "30")
        self.assertEqual(superheroinfo.powerstats[0].durability, "40")
        self.assertEqual(superheroinfo.powerstats[0].power, "50")
        self.assertEqual(superheroinfo.powerstats[0].combat, "60")


    def test_invalid_powerstats_model(self):
        
        superheroinfo = SuperheroInfo(
            name="Batman"
        )

        powerstats = Powerstats(
            intelligence=None, 
            strength=None, 
            speed=None, 
            durability=None, 
            power=None, 
            combat=None)

        superheroinfo.powerstats.append(powerstats)
        self.testuser.superheros.append(superheroinfo)

        db.session.add(superheroinfo, powerstats)

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()