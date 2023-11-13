import unittest
from flask import Flask, session
from app import app, db
from models_forms.models import *

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sr_test_db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_start_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_route(self):
        # Assuming you have a test user created for this test
        test_user = User(username='testuser', password='testpassword', summoner_name='Brendinoo')
        db.session.add(test_user)
        db.session.commit()

        response = self.app.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertEqual(session['curr_user'], test_user.puuid)

    def test_logout_route(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['curr_user'] = 'some_fake_user_puuid'

            response = client.get('/logout')
            self.assertEqual(response.status_code, 302)  # Redirect after logout
            self.assertNotIn('curr_user', session)

    # You can add more tests for other routes similarly

if __name__ == '__main__':
    unittest.main()
