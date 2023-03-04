"""Favorites view tests."""

import os, requests, json

from unittest import TestCase

from models import db, connect_db, User, Superheros, MySuperheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections 
from api import API_KEY 

os.environ['DATABASE_URL'] = "postgresql:///superhero-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class FavoritesViewTestCase(TestCase):
    """Test views for favorites."""

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

    def test_view_favorites(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = requests.get(f"{API_KEY}/search/Batman")      
            data = res.json()

            id_1 = data['results'][0]['id']
            id_2 = data['results'][1]['id']
            id_3 = data['results'][2]['id']

            resp = c.post(f"/api/superhero/{id_1}/add", follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Superhero (Batman) added!", str(resp.data))   

            resp = c.post(f"/api/superhero/{id_2}/add", follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Superhero (Batman) added!", str(resp.data))   

            resp = c.post(f"/api/superhero/{id_3}/add", follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Superhero (Batman II) added!", str(resp.data))   

            resp = c.get("/favorites/view")

            self.assertIn("Name: Batman", str(resp.data))   
            self.assertIn("Name: Batman", str(resp.data))   
            self.assertIn("Name: Batman II", str(resp.data))   

    def test_view_favorites_search(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = requests.get(f"{API_KEY}/search/Batman")      
            data = res.json()

            id_1 = data['results'][0]['id']
            id_2 = data['results'][1]['id']
            id_3 = data['results'][2]['id']

            resp = c.post(f"/api/superhero/{id_1}/add", follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Superhero (Batman) added!", str(resp.data))   

            resp = c.post(f"/api/superhero/{id_2}/add", follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Superhero (Batman) added!", str(resp.data))   

            resp = c.post(f"/api/superhero/{id_3}/add", follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Superhero (Batman II) added!", str(resp.data))   

            resp = c.post("/favorites/view", data={"name": "Batman", "order": "desc"})

            self.assertIn("Name: Batman", str(resp.data))   
            self.assertIn("Name: Batman", str(resp.data))   
            self.assertIn("Name: Batman II", str(resp.data))   

    def test_view_favorites_by_superhero_Id(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = requests.get(f"{API_KEY}/search/Batman")      
            data = res.json()

            id_1 = data['results'][0]['id']
            id_2 = data['results'][1]['id']

            resp = c.post(f"/api/superhero/{id_1}/add", follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Superhero (Batman) added!", str(resp.data))   

            resp = c.post(f"/api/superhero/{id_2}/add", follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Superhero (Batman) added!", str(resp.data))   

            resp = c.get("/favorites/view/1")

            self.assertEqual(res.status_code, 200)
            self.assertIn("Name: Batman", str(resp.data))   
            self.assertIn("Full-name: Terry McGinnis", str(resp.data))   
            self.assertIn("Intelligence: 81", str(resp.data))   
            self.assertIn("Gender: Male", str(resp.data))   
            self.assertIn("Occupation: -", str(resp.data))   
            self.assertIn("Group-affiliation: Batman Family, Justice League Unlimited", str(resp.data))   

            resp = c.get("/favorites/view/2")

            self.assertEqual(res.status_code, 200)
            self.assertIn("Name: Batman", str(resp.data))   
            self.assertIn("Full-name: Bruce Wayne", str(resp.data))   
            self.assertIn("Intelligence: 100", str(resp.data))   
            self.assertIn("Gender: Male", str(resp.data))   
            self.assertIn("Occupation: Businessman", str(resp.data))   
            self.assertIn("Group-affiliation: Batman Family", str(resp.data))   

    def test_delete_superhero_from_favorites(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1_id

            res = requests.get(f"{API_KEY}/search/Batman")      
            data = res.json()

            id = data['results'][0]['id']

            resp = c.post(f"/api/superhero/{id}/add", follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Superhero (Batman) added!", str(resp.data))   

            resp = c.post("/favorites/delete/1", follow_redirects=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Deleted superhero from list", str(resp.data))   
            self.assertNotIn("Batman", str(resp.data))    