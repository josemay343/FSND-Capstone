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

        self.error_new_vehicle = {
            'make': '',
            'model': 'test',
            'year': 2001,
            'color': 'red'
        }

        self.error_new_sale = {
            'customer_id': '',
            'vehicle_id': ''
        }
        self.error_new_customer = {
            'first_name': '',
            'last_name': 'test',
            'phone_number': '1234',
            'address': 'test'
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

    def test_422_post_vehicles(self):
        res = self.client().post('/vehicles', json=self.error_new_vehicle)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_sales(self):
        res = self.client().get('/sales')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['sales'])

    def test_422_post_sales(self):
        res = self.client().post('/sales', json=self.error_new_sale)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_customers(self):
        res = self.client().get('/customers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['customers'])

    def test_422_post_customers(self):
        res = self.client().post('/customers', json=self.error_new_customer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()