"""Users view tests."""

import os
from unittest import TestCase

from models import db, connect_db, User, Superheros, MySuperheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections 

os.environ['DATABASE_URL'] = "postgresql:///superhero-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UsersViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.user1 = User.signup("John", "Smith", "testing1", "password")
        self.user1_id = 1111
        self.user1.id = self.user1_id

        self.user2 = User.signup("Ken", "Smith", "testing2", "password")
        self.user2_id = 2222
        self.user2.id = self.user2_id

        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_profile(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.get(f"/user/{self.user1_id}")

            self.assertIn("Username: testing1", str(res.data))

    def test_user_edit_profile(self):
         with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post(f"/user/edit/{self.user1_id}", data={"first_name": "Johnny", 
                                                            "last_name": "Davis", 
                                                            "username": "johnny123", 
                                                            "password": "password",
                                                            "image_url": "cat"},
                                                            follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Username: johnny123", str(res.data))       

    def test_user_search_superheros(self):
         with self.client as c:
            superheroinfo_1 = SuperheroInfo(name="batman")
            superheroinfo_2 = SuperheroInfo(name="batman 2")
            self.user2.mysuperheros.append(superheroinfo_1)
            self.user2.mysuperheros.append(superheroinfo_2)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/users/search", data={"name": "batman"})

            self.assertEqual(res.status_code, 200)
            self.assertIn("Name: batman", str(res.data))       
            self.assertIn("Name: batman 2", str(res.data))       

    def test_user_invaild_search_superheros(self):
         with self.client as c:
            superheroinfo = SuperheroInfo(name="batman")
            self.user2.mysuperheros.append(superheroinfo)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/users/search", data={"name": "superman"}, follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("No superhero found with that name", str(res.data))       

    def test_view_superheros_by_other_users(self):
         with self.client as c:
            superheroinfo = SuperheroInfo(name="batman")

            powerstats = Powerstats(
            intelligence="10", 
            strength="20", 
            speed="30", 
            durability="40", 
            power="50", 
            combat="60")

            biography = Biography(
            full_name="Batman 1", 
            place_of_birth="NY", 
            first_appearance="Maine", 
            alter_egos="No alter egos", 
            publisher="DC")

            appearance = Appearance(
            gender="Male", 
            race="White", 
            height="5'9", 
            weight="120lb", 
            eye_color="Black",
            hair_color="Black")

            work = Work(
            occupation="hero", 
            base_of_operation="NA")

            connections = Connections(
            group_affiliation="group", 
            relatives="relatives")

            superheroinfo.powerstats.append(powerstats)
            superheroinfo.biography.append(biography)
            superheroinfo.appearance.append(appearance)
            superheroinfo.work.append(work)
            superheroinfo.connections.append(connections)

            self.user2.mysuperheros.append(superheroinfo)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.get("/users/view/superhero/1")

            self.assertEqual(res.status_code, 200)
            self.assertIn("Name: batman", str(res.data))   
            self.assertIn("Full-name: Batman 1", str(res.data))   
            self.assertIn("Intelligence: 10", str(res.data))   
            self.assertIn("Gender: Male", str(res.data))   
            self.assertIn("Occupation: hero", str(res.data))   
            self.assertIn("Group-affiliation: group", str(res.data))   

    def test_add_superheros_by_other_users(self):
         with self.client as c:
            superheroinfo = SuperheroInfo(name="batman")

            powerstats = Powerstats(
            intelligence="10", 
            strength="20", 
            speed="30", 
            durability="40", 
            power="50", 
            combat="60")

            biography = Biography(
            full_name="Batman 1", 
            place_of_birth="NY", 
            first_appearance="Maine", 
            alter_egos="No alter egos", 
            publisher="DC")

            appearance = Appearance(
            gender="Male", 
            race="White", 
            height="5'9", 
            weight="120lb", 
            eye_color="Black",
            hair_color="Black")

            work = Work(
            occupation="hero", 
            base_of_operation="NA")

            connections = Connections(
            group_affiliation="group", 
            relatives="relatives")

            superheroinfo.powerstats.append(powerstats)
            superheroinfo.biography.append(biography)
            superheroinfo.appearance.append(appearance)
            superheroinfo.work.append(work)
            superheroinfo.connections.append(connections)

            self.user2.mysuperheros.append(superheroinfo)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/users/add/superhero/1", follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Superhero (batman) added!", str(res.data))   

    def test_duplicate_superhero_added(self):
         with self.client as c:
            superheroinfo = SuperheroInfo(name="batman")

            powerstats = Powerstats(
            intelligence="10", 
            strength="20", 
            speed="30", 
            durability="40", 
            power="50", 
            combat="60")

            biography = Biography(
            full_name="Batman 1", 
            place_of_birth="NY", 
            first_appearance="Maine", 
            alter_egos="No alter egos", 
            publisher="DC")

            appearance = Appearance(
            gender="Male", 
            race="White", 
            height="5'9", 
            weight="120lb", 
            eye_color="Black",
            hair_color="Black")

            work = Work(
            occupation="hero", 
            base_of_operation="NA")

            connections = Connections(
            group_affiliation="group", 
            relatives="relatives")

            superheroinfo.powerstats.append(powerstats)
            superheroinfo.biography.append(biography)
            superheroinfo.appearance.append(appearance)
            superheroinfo.work.append(work)
            superheroinfo.connections.append(connections)

            self.user2.mysuperheros.append(superheroinfo)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/users/add/superhero/1", follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Superhero (batman) added!", str(res.data))   

            res = c.post("/users/add/superhero/1", follow_redirects=True)
            self.assertIn("Superhero already in favorties", str(res.data))   
