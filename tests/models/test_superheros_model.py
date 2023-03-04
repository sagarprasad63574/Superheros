"""Superheros model tests."""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Superheros, MySuperheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections 

os.environ['DATABASE_URL'] = "postgresql:///superhero-test"

from app import app

db.create_all()


class SuperherosModelTestCase(TestCase):
    """Test model for superheros."""

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

    def test_superheros(self):
        
        superheroinfo = SuperheroInfo(
            name="Batman"
        )

        self.testuser.superheros.append(superheroinfo)
        db.session.commit()

        self.assertEqual(len(self.testuser.superheros), 1)
        self.assertEqual(self.testuser.superheros[0].name, "Batman")

        superheros = db.session.query(Superheros).all()
        self.assertEqual(len(superheros), 1)
        self.assertEqual(superheros[0].superheroinfo_id, superheroinfo.id)
        self.assertEqual(superheros[0].user_id, self.testuser_id)

    def test_invalid_superheros(self):
        
        superheroinfo = SuperheroInfo(
            name="Batman"
        )

        db.session.add(superheroinfo)
        db.session.commit()

        self.assertNotEqual(len(self.testuser.superheros), 1)

        superheros = db.session.query(Superheros).all()
        self.assertNotEqual(len(superheros), 1)

    def test_many_superheros(self):
        
        superheroinfo_1 = SuperheroInfo(
            name="Batman"
        )

        superheroinfo_2 = SuperheroInfo(
            name="Batman 2"
        )

        self.testuser.superheros.append(superheroinfo_1)
        self.testuser.superheros.append(superheroinfo_2)

        db.session.commit()

        self.assertEqual(len(self.testuser.superheros), 2)
        self.assertEqual(self.testuser.superheros[0].name, "Batman")
        self.assertEqual(self.testuser.superheros[1].name, "Batman 2")

        superheros = db.session.query(Superheros).all()
        self.assertEqual(len(superheros), 2)
        self.assertEqual(superheros[0].superheroinfo_id, superheroinfo_1.id)
        self.assertEqual(superheros[0].user_id, self.testuser_id)
        self.assertEqual(superheros[1].superheroinfo_id, superheroinfo_2.id)
        self.assertEqual(superheros[1].user_id, self.testuser_id)

    def test_duplicate_superhero_ids(self):
        
        superheroinfo_1 = SuperheroInfo(
            superhero_id="10",
            name="Batman"
        )

        superheroinfo_2 = SuperheroInfo(
            superhero_id="10",
            name="Batman"
        )

        self.testuser.superheros.append(superheroinfo_1)
        self.testuser.superheros.append(superheroinfo_2)

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_add_powerstats_to_superhero(self):
        
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

        superheros = db.session.query(Superheros).all()

        self.assertEqual(len(superheros), 1)
        self.assertEqual(superheros[0].superheroinfo_id, superheroinfo.id)
        self.assertEqual(superheros[0].user_id, self.testuser_id)
        self.assertEqual(len(superheros[0].superheroinfo.powerstats), 1)
        self.assertEqual(superheros[0].superheroinfo.powerstats[0].intelligence, "10")
        self.assertEqual(superheros[0].superheroinfo.powerstats[0].strength, "20")
        self.assertEqual(superheros[0].superheroinfo.powerstats[0].speed, "30")
        self.assertEqual(superheros[0].superheroinfo.powerstats[0].durability, "40")
        self.assertEqual(superheros[0].superheroinfo.powerstats[0].power, "50")
        self.assertEqual(superheros[0].superheroinfo.powerstats[0].combat, "60")


    def test_add_biography_to_superhero(self):
        
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

        superheros = db.session.query(Superheros).all()

        self.assertEqual(len(superheros), 1)
        self.assertEqual(superheros[0].superheroinfo_id, superheroinfo.id)
        self.assertEqual(superheros[0].user_id, self.testuser_id)
        self.assertEqual(len(superheros[0].superheroinfo.biography), 1)
        self.assertEqual(superheros[0].superheroinfo.biography[0].full_name, "Batman 1")
        self.assertEqual(superheros[0].superheroinfo.biography[0].place_of_birth, "NY")
        self.assertEqual(superheros[0].superheroinfo.biography[0].first_appearance, "Maine")
        self.assertEqual(superheros[0].superheroinfo.biography[0].alter_egos, "No alter egos")
        self.assertEqual(superheros[0].superheroinfo.biography[0].publisher, "DC")

    def test_add_appearance_to_superhero(self):
        
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

        superheros = db.session.query(Superheros).all()

        self.assertEqual(len(superheros), 1)
        self.assertEqual(superheros[0].superheroinfo_id, superheroinfo.id)
        self.assertEqual(superheros[0].user_id, self.testuser_id)
        self.assertEqual(len(superheros[0].superheroinfo.appearance), 1)
        self.assertEqual(superheros[0].superheroinfo.appearance[0].gender, "Male")
        self.assertEqual(superheros[0].superheroinfo.appearance[0].race, "White")
        self.assertEqual(superheros[0].superheroinfo.appearance[0].height, "5'9")
        self.assertEqual(superheros[0].superheroinfo.appearance[0].weight, "120lb")
        self.assertEqual(superheros[0].superheroinfo.appearance[0].eye_color, "Black")
        self.assertEqual(superheros[0].superheroinfo.appearance[0].hair_color, "Black")

    def test_add_work_to_superhero(self):
        
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

        superheros = db.session.query(Superheros).all()

        self.assertEqual(len(superheros), 1)
        self.assertEqual(superheros[0].superheroinfo_id, superheroinfo.id)
        self.assertEqual(superheros[0].user_id, self.testuser_id)
        self.assertEqual(len(superheros[0].superheroinfo.work), 1)
        self.assertEqual(superheros[0].superheroinfo.work[0].occupation, "hero")
        self.assertEqual(superheros[0].superheroinfo.work[0].base_of_operation, "NA")

    def test_add_connections_to_superhero(self):
        
        superheroinfo = SuperheroInfo(
            name="Batman"
        )

        connections = Connections(
            group_affiliation="group", 
            relatives="relatives")

        superheroinfo.connections.append(connections)
        self.testuser.superheros.append(superheroinfo)

        db.session.add(superheroinfo, connections)
        db.session.commit()

        self.assertEqual(len(self.testuser.superheros), 1)
        self.assertEqual(self.testuser.superheros[0].name, "Batman")
        self.assertEqual(len(superheroinfo.connections), 1)
        self.assertEqual(connections.superheroinfo_id, superheroinfo.id)
        
        superheros = db.session.query(Superheros).all()

        self.assertEqual(len(superheros), 1)
        self.assertEqual(superheros[0].superheroinfo_id, superheroinfo.id)
        self.assertEqual(superheros[0].user_id, self.testuser_id)
        self.assertEqual(len(superheros[0].superheroinfo.connections), 1)
        self.assertEqual(superheros[0].superheroinfo.connections[0].group_affiliation, "group")
        self.assertEqual(superheros[0].superheroinfo.connections[0].relatives, "relatives")