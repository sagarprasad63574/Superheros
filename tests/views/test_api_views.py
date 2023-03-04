"""API view tests."""

import os, requests, json

from unittest import TestCase

from models import db, connect_db, User, Superheros, MySuperheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections 
from api import API_KEY 

os.environ['DATABASE_URL'] = "postgresql:///superhero-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class APIViewTestCase(TestCase):
    """Test views for API."""

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

    def test_api_search(self):
         with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/api/search", data={"name": "Batman"})

            self.assertEqual(res.status_code, 200)
            self.assertIn("Name: Batman", str(res.data))  
            self.assertIn("Name: Batman II", str(res.data))  

    def test_api_invaild_search(self):
         with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = c.post("/api/search", data={"name": "dance"})

            self.assertEqual(res.status_code, 200)
            self.assertIn("No superhero found with that name", str(res.data))  

    def test_api_superhero_view(self):
         with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = requests.get(f"{API_KEY}/search/Batman")      
            data = res.json()

            id = data['results'][0]['id']

            resp = c.get(f"/api/superhero/{id}/view")
            self.assertEqual(res.status_code, 200)
            self.assertIn("Name: Batman", str(resp.data))   
            self.assertIn("Full-name: Terry McGinnis", str(resp.data))   
            self.assertIn("Intelligence: 81", str(resp.data))   
            self.assertIn("Gender: Male", str(resp.data))   
            self.assertIn("Occupation: -", str(resp.data))   
            self.assertIn("Group-affiliation: Batman Family, Justice League Unlimited", str(resp.data))   

    def test_api_superhero_add(self):
         with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = requests.get(f"{API_KEY}/search/Batman")      
            data = res.json()

            id = data['results'][0]['id']

            resp = c.post(f"/api/superhero/{id}/add", follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Superhero (Batman) added!", str(resp.data))   

    def test_api_superhero_duplicate_add(self):
         with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = requests.get(f"{API_KEY}/search/Batman")      
            data = res.json()

            id = data['results'][0]['id']

            resp = c.post(f"/api/superhero/{id}/add", follow_redirects=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn("Superhero (Batman) added!", str(resp.data))   

            resp = c.post(f"/api/superhero/{id}/add", follow_redirects=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn("Superhero already in the list", str(resp.data))   

    def test_api_superhero_add_2(self):
         with self.client as c:
            res = requests.get(f"{API_KEY}/search/Batman")      
            data = res.json()

            superheroinfo = SuperheroInfo(
                    superhero_id=data['results'][0]['id'], 
                    name=data['results'][0]['name'], 
                    image_url=data['results'][0]['image']['url'])

            powerstats = Powerstats(
                intelligence=data['results'][0]['powerstats']['intelligence'], 
                strength=data['results'][0]['powerstats']['strength'], 
                speed=data['results'][0]['powerstats']['speed'], 
                durability=data['results'][0]['powerstats']['durability'], 
                power=data['results'][0]['powerstats']['power'], 
                combat=data['results'][0]['powerstats']['combat'])

            biography = Biography(
                full_name=data['results'][0]['biography']['full-name'], 
                place_of_birth=data['results'][0]['biography']['place-of-birth'], 
                first_appearance=data['results'][0]['biography']['first-appearance'], 
                alter_egos=data['results'][0]['biography']['alter-egos'], 
                publisher=data['results'][0]['biography']['publisher'])

            appearance = Appearance(
                gender=data['results'][0]['appearance']['gender'], 
                race=data['results'][0]['appearance']['race'], 
                height=data['results'][0]['appearance']['height'][0], 
                weight=data['results'][0]['appearance']['weight'][0], 
                eye_color=data['results'][0]['appearance']['eye-color'],
                hair_color=data['results'][0]['appearance']['hair-color'])
            
            work = Work(
                occupation=data['results'][0]['work']['occupation'], 
                base_of_operation=data['results'][0]['work']['base'])

            connections = Connections(
                group_affiliation=data['results'][0]['connections']['group-affiliation'], 
                relatives=data['results'][0]['connections']['relatives'])

            superheroinfo.powerstats.append(powerstats)
            superheroinfo.biography.append(biography)
            superheroinfo.appearance.append(appearance)
            superheroinfo.work.append(work)
            superheroinfo.connections.append(connections)

            superhero = [superheroinfo, powerstats, biography, appearance, work, connections]

            db.session.add_all(superhero)
            db.session.commit()

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = requests.get(f"{API_KEY}/search/Batman")      
            data = res.json()

            id = data['results'][0]['id']

            resp = c.post(f"/api/superhero/{id}/add", follow_redirects=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn("Superhero (Batman) added!", str(resp.data))     