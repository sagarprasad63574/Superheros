"""Mylist view tests."""

import os, requests, json

from unittest import TestCase

from models import db, connect_db, User, Superheros, MySuperheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections 
from api import API_KEY 

os.environ['DATABASE_URL'] = "postgresql:///superhero-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class MylistViewTestCase(TestCase):
    """Test views for mylist."""

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

    def test_view_create_superhero(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id
            
            res = c.get("/mylist/create")

            self.assertEqual(res.status_code, 200)
            self.assertIn("Enter name of superhero", str(res.data))  

    def test_create_superhero(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id
            
            res = c.post("/mylist/create", data={"name": "New hero", "image_url": ""}, follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Name: New hero", str(res.data))   

    def test_view_superheros(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id
            
            res = c.post("/mylist/create", data={"name": "New hero", "image_url": ""}, follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Name: New hero", str(res.data))   

            res = c.post("/mylist/create", data={"name": "New hero 2", "image_url": ""}, follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Name: New hero 2", str(res.data))  

            res = c.get("/mylist/view")

            self.assertEqual(res.status_code, 200)
            self.assertIn("Name: New hero", str(res.data))  
            self.assertIn("Name: New hero 2", str(res.data))  

    def test_view_superheros_search(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id
            
            res = c.post("/mylist/create", data={"name": "New hero", "image_url": ""}, follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Name: New hero", str(res.data))   

            res = c.post("/mylist/create", data={"name": "New hero 2", "image_url": ""}, follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Name: New hero 2", str(res.data))  

            res = c.post("/mylist/view", data={"name": "New hero", "order": "desc"})

            self.assertEqual(res.status_code, 200)
            self.assertIn("Name: New hero", str(res.data))  
            self.assertIn("Name: New hero 2", str(res.data))  

    def test_view_superhero_by_id(self):
         with self.client as c:

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

            self.user1.mysuperheros.append(superheroinfo)

            superhero = [superheroinfo, powerstats, biography, appearance, work, connections]

            db.session.add_all(superhero)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.get("/mylist/view/1")
            self.assertEqual(res.status_code, 200)
            self.assertIn("Name: Batman", str(res.data))  


    def test_edit_superhero_image(self):
         with self.client as c:

            superheroinfo = SuperheroInfo(
                name="Batman"
            )

            self.user1.mysuperheros.append(superheroinfo)
            db.session.add(superheroinfo)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/mylist/edit/image_url/1", data={"image_url": ""}, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Image: None", str(res.data))  

    def test_add_superhero_powerstats(self):
         with self.client as c:

            superheroinfo = SuperheroInfo(
                name="Batman"
            )

            self.user1.mysuperheros.append(superheroinfo)

            db.session.add(superheroinfo)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/mylist/add/powerstats/1", data={"intelligence": "10", 
                                                            "strength": "20", 
                                                            "speed": "30", 
                                                            "durability": "40",
                                                            "power": "50",
                                                            "combat": "60"}, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Powerstats:", str(res.data))  
            self.assertIn("Intelligence: 10", str(res.data))  
            self.assertIn("Strength: 20", str(res.data))  
            self.assertIn("Speed: 30", str(res.data))  
            self.assertIn("Durability: 40", str(res.data))  
            self.assertIn("Power: 50", str(res.data))  
            self.assertIn("Combat: 60", str(res.data))  

    def test_edit_superhero_powerstats(self):
         with self.client as c:

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

            self.user1.mysuperheros.append(superheroinfo)

            superhero = [superheroinfo, powerstats]

            db.session.add_all(superhero)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/mylist/edit/powerstats/1", data={"intelligence": "90", 
                                                            "strength": "80", 
                                                            "speed": "70", 
                                                            "durability": "60",
                                                            "power": "50",
                                                            "combat": "40"}, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Powerstats:", str(res.data))  
            self.assertIn("Intelligence: 90", str(res.data))  
            self.assertIn("Strength: 80", str(res.data))  
            self.assertIn("Speed: 70", str(res.data))  
            self.assertIn("Durability: 60", str(res.data))  
            self.assertIn("Power: 50", str(res.data))  
            self.assertIn("Combat: 40", str(res.data))  

    def test_add_superhero_biography(self):
         with self.client as c:

            superheroinfo = SuperheroInfo(
                name="Batman"
            )

            self.user1.mysuperheros.append(superheroinfo)

            db.session.add(superheroinfo)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/mylist/add/biography/1", data={"full_name": "Batman 1", 
                                                        "place_of_birth": "NY", 
                                                        "first_appearance": "Maine", 
                                                        "alter_egos": "No alter egos", 
                                                        "publisher": "DC"}, follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Biography:", str(res.data))  
            self.assertIn("Full-name: Batman 1", str(res.data))  
            self.assertIn("Place-of-birth: NY", str(res.data))  
            self.assertIn("First-appearance: Maine", str(res.data))  
            self.assertIn("Alter-egos: No alter egos", str(res.data))  
            self.assertIn("Publisher: DC", str(res.data))  

    def test_edit_superhero_biography(self):
         with self.client as c:

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

            self.user1.mysuperheros.append(superheroinfo)

            superhero = [superheroinfo, biography]

            db.session.add_all(superhero)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/mylist/edit/biography/1", data={"full_name": "Batman 2", 
                                                        "place_of_birth": "CA", 
                                                        "first_appearance": "Seaside", 
                                                        "alter_egos": "No alter egos", 
                                                        "publisher": "AB"}, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Biography:", str(res.data))  
            self.assertIn("Full-name: Batman 2", str(res.data))  
            self.assertIn("Place-of-birth: CA", str(res.data))  
            self.assertIn("First-appearance: Seaside", str(res.data))  
            self.assertIn("Alter-egos: No alter egos", str(res.data))  
            self.assertIn("Publisher: AB", str(res.data))  

    def test_add_superhero_appearance(self):
         with self.client as c:

            superheroinfo = SuperheroInfo(
                name="Batman"
            )

            self.user1.mysuperheros.append(superheroinfo)

            db.session.add(superheroinfo)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/mylist/add/appearance/1", data={"gender": "Male", 
                                                        "race": "White", 
                                                        "height": "5'9", 
                                                        "weight": "120lb", 
                                                        "eye_color": "Black",
                                                        "hair_color": "Black"}, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Appearance:", str(res.data))  
            self.assertIn("Gender: Male", str(res.data))  
            self.assertIn("Race: White", str(res.data))  
            self.assertIn("Height: 5&#39;9", str(res.data))  
            self.assertIn("Weight: 120lb", str(res.data))  
            self.assertIn("Eye-color: Black", str(res.data))  
            self.assertIn("Hair-color: Black", str(res.data))  

    def test_edit_superhero_appearance(self):
         with self.client as c:

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

            self.user1.mysuperheros.append(superheroinfo)

            superhero = [superheroinfo, appearance]

            db.session.add_all(superhero)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/mylist/edit/appearance/1", data={"gender": "Female", 
                                                        "race": "NA", 
                                                        "height": "5'10", 
                                                        "weight": "140lb", 
                                                        "eye_color": "White",
                                                        "hair_color": "White"}, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Appearance:", str(res.data))  
            self.assertIn("Gender: Female", str(res.data))  
            self.assertIn("Race: NA", str(res.data))  
            self.assertIn("Height: 5&#39;10", str(res.data))  
            self.assertIn("Weight: 140lb", str(res.data))  
            self.assertIn("Eye-color: White", str(res.data))  
            self.assertIn("Hair-color: White", str(res.data))  

    def test_add_superhero_work(self):
         with self.client as c:

            superheroinfo = SuperheroInfo(
                name="Batman"
            )

            self.user1.mysuperheros.append(superheroinfo)

            db.session.add(superheroinfo)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/mylist/add/work/1", data={"occupation": "hero", 
                                                        "base_of_operation": "NA"}, follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Work:", str(res.data))  
            self.assertIn("Occupation: hero", str(res.data))  
            self.assertIn("Base: NA", str(res.data))  

    def test_edit_superhero_work(self):
         with self.client as c:

            superheroinfo = SuperheroInfo(
                name="Batman"
            )

            work = Work(
                occupation="hero", 
                base_of_operation="NA")

            superheroinfo.work.append(work)

            self.user1.mysuperheros.append(superheroinfo)

            superhero = [superheroinfo, work]

            db.session.add_all(superhero)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/mylist/edit/work/1", data={"occupation": "NA", 
                                                        "base_of_operation": "NY"}, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Work:", str(res.data))  
            self.assertIn("Occupation: NA", str(res.data))  
            self.assertIn("Base: NY", str(res.data))  

    def test_add_superhero_connections(self):
         with self.client as c:

            superheroinfo = SuperheroInfo(
                name="Batman"
            )

            self.user1.mysuperheros.append(superheroinfo)

            db.session.add(superheroinfo)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/mylist/add/connections/1", data={"group_affiliation": "group", 
                                                        "relatives": "relatives"}, follow_redirects=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn("Connections:", str(res.data))  
            self.assertIn("Group-affiliation: group", str(res.data))  
            self.assertIn("Relatives: relatives", str(res.data))    

    def test_edit_superhero_connections(self):
        with self.client as c:

            superheroinfo = SuperheroInfo(
                name="Batman"
            )

            connections = Connections(
                group_affiliation="group", 
                relatives="relatives")

            superheroinfo.connections.append(connections)

            self.user1.mysuperheros.append(superheroinfo)

            superhero = [superheroinfo, connections]

            db.session.add_all(superhero)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/mylist/edit/connections/1", data={"group_affiliation": "new group", 
                                                        "relatives": "new relatives"}, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Connections:", str(res.data))  
            self.assertIn("Group-affiliation: new group", str(res.data))  
            self.assertIn("Relatives: new relatives", str(res.data))   


    def test_delete_superhero_from_mylist(self):
        with self.client as c:

            superheroinfo = SuperheroInfo(
                name="Batman"
            )

            self.user1.mysuperheros.append(superheroinfo)

            db.session.add(superheroinfo)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/mylist/delete/1", follow_redirects=True)

            self.assertEqual(res.status_code, 200)            
            self.assertIn("Deleted superhero from list", str(res.data))   
            self.assertNotIn("Batman", str(res.data))    