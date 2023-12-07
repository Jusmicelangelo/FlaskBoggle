from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        # Make Flask errors be real errors, not HTML pages with error info
        app.config['TESTING'] = True

    def test_session(self):
        """necessary info in session and on html"""

        with self.client:
            resp = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('number_of_plays'))

    def test_valid_word(self):
        """Test if word is valid by drawn board"""

        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["Y", "O", "U", "A", "B"], 
                                 ["Y", "O", "U", "A", "B"], 
                                 ["Y", "O", "U", "A", "B"], 
                                 ["Y", "O", "U", "A", "B"], 
                                 ["Y", "O", "U", "A", "B"]]
        response = self.client.get('/word-check?word=you')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        self.client.get('/')
        response = self.client.get('/word-check?word=unbelievable')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.get(
            '/word-check?word=herrje')
        self.assertEqual(response.json['result'], 'not-word')

