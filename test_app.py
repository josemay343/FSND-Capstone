import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *

class DealershipTestCase(unittest.TestCase):
    """This class represents the Dealership app test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "dealership_test"
        self.database_path = "postgresql://{}@{}/{}".format(
            'yosef', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_vehicle = {
            'make': 'test',
            'model': 'test',
            'year': 2000,
            'color': 'test',
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_vehicles(self):
        res = self.client().get('/vehicles')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['vehicles'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()