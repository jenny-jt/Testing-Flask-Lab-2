import unittest

from party import app
from model import db, example_data, connect_to_db
from flask import Flask, session, render_template, request, flash, redirect


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        # FIXME: Add a test to show we see the RSVP form, but NOT the
        result = self.client.get("/")
        self.assertIn(b"Please RSVP", result.data)
        # party details

    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)
        self.assertIn(b"Party Details", result.data)                          
        # FIXME: Once we RSVP, we should see the party details, but
        # not the RSVP form


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "itsasecret"
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True

        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_games(self):
        # FIXME: test that the games page displays the game from example_data()
        result = self.client.get("/games")
        self.assertIn(b"ex_game", result.data)


if __name__ == "__main__":
    unittest.main()
