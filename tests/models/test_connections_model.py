"""Connections model tests."""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Superheros, MySuperheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections 

os.environ['DATABASE_URL'] = "postgresql:///superhero-test"

from app import app

db.create_all()


class ConnectionsModelTestCase(TestCase):
    """Test model for connections."""

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

    def test_add_connections_to_superheros(self):
        
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
        self.assertEqual(superheroinfo.connections[0].group_affiliation, "group")
        self.assertEqual(superheroinfo.connections[0].relatives, "relatives")

    def test_add_connections_to_mysuperheros(self):

        superheroinfo = SuperheroInfo(
            name="Batman"
        )

        connections = Connections(
            group_affiliation="group", 
            relatives="relatives")

        superheroinfo.connections.append(connections)
        self.testuser.mysuperheros.append(superheroinfo)

        db.session.add(superheroinfo, connections)
        db.session.commit()

        self.assertEqual(len(self.testuser.mysuperheros), 1)
        self.assertEqual(self.testuser.mysuperheros[0].name, "Batman")
        self.assertEqual(len(superheroinfo.connections), 1)
        self.assertEqual(connections.superheroinfo_id, superheroinfo.id)
        self.assertEqual(superheroinfo.connections[0].group_affiliation, "group")
        self.assertEqual(superheroinfo.connections[0].relatives, "relatives")