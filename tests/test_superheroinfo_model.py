"""Superheroinfo model tests."""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Superheros, MySuperheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections 

os.environ['DATABASE_URL'] = "postgresql:///superhero-test"

from app import app

db.create_all()


class SuperheroInfoModelTestCase(TestCase):
    """Test views for superheroinfos."""

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

    def test_superherinfo_model(self):
        
        superheroinfo = SuperheroInfo(
            name="Batman"
        )

        self.testuser.superheros.append(superheroinfo)
        db.session.commit()

        self.assertEqual(len(self.testuser.superheros), 1)
        self.assertEqual(self.testuser.superheros[0].name, "Batman")

    def test_add_powerstats_to_superhero(self):
        
        superheroinfo = SuperheroInfo(
            name="Batman"
        )

        powerstat = Powerstats(
            intelligence="10", 
            strength="20", 
            speed="30", 
            durability="40", 
            power="50", 
            combat="60")

        superheroinfo.powerstats.append(powerstat)
        self.testuser.superheros.append(superheroinfo)

        db.session.add(superheroinfo, powerstat)
        db.session.commit()

        self.assertEqual(len(self.testuser.superheros), 1)
        self.assertEqual(self.testuser.superheros[0].name, "Batman")
        self.assertEqual(len(superheroinfo.powerstats), 1)
        self.assertEqual(powerstat.superheroinfo_id, superheroinfo.id)
        self.assertEqual(superheroinfo.powerstat[0].intelligence, "10")
        self.assertEqual(superheroinfo.powerstat[0].strength, "20")
        self.assertEqual(superheroinfo.powerstat[0].speed, "30")
        self.assertEqual(superheroinfo.powerstat[0].durability, "40")
        self.assertEqual(superheroinfo.powerstat[0].power, "50")
        self.assertEqual(superheroinfo.powerstat[0].combat, "60")


    def test_add_powerstats_to_superhero(self):
        
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


    # def test_message_likes(self):
    #     m1 = Message(
    #         text="Test message",
    #         user_id=self.testuser_id
    #     )

    #     m2 = Message(
    #         text="Test message 2",
    #         user_id=self.testuser_id 
    #     )

    #     user = User.signup("test2", "test2@gmail.com", "password", None)
    #     user_id = 1111
    #     user.id = user_id
    #     db.session.add_all([m1, m2, user])
    #     db.session.commit()

    #     user.likes.append(m1)

    #     db.session.commit()

    #     l = Likes.query.filter(Likes.user_id == user_id).all()
    #     self.assertEqual(len(l), 1)
    #     self.assertEqual(l[0].message_id, m1.id)
