import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db

class YieldifyTestCase(unittest.TestCase):
    """This class represents the yieldify test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "yieldifydb_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                       self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)


    def tearDown(self):
        # Executed after reach test

        pass

    def test_unavailable_endpoint(self):
        res = self.client().get('/interview')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_error_405_get_browser_stats(self):
        """Test wrong method to GET all browser stats """

        res = self.client().post('/stats/browser')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "method not allowed")
        self.assertEqual(data['success'], False)

    def test_error_405_get_os_stats(self):
        """Test wrong method to GET all browser stats """

        res = self.client().post('/stats/os')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "method not allowed")
        self.assertEqual(data['success'], False)

    def test_error_405_get_device_stats(self):
        """Test wrong method to GET all browser stats """

        res = self.client().post('/stats/device')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "method not allowed")
        self.assertEqual(data['success'], False)


    def test_error_400_get_device_stats(self):
        """Test out of bound start and end date """

        res = self.client().get('/stats/device?start_date=2020-01-01&end_date=2020-02-01')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(data['success'], False)

    def test_error_400_get_os_stats(self):
        """Test out of bound start and end date """

        res = self.client().get('/stats/os?start_date=2020-01-01&end_date=2020-02-01')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(data['success'], False)

    def test_error_400_get_browser_stats(self):
        """Test out of bound start and end date """

        res = self.client().get('/stats/browser?start_date=2020-01-01&end_date=2020-02-01')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request")
        self.assertEqual(data['success'], False)

    def test_200_get_browser_stats(self):
        """Test wrong method to GET all browser stats """

        res = self.client().get('/stats/browser')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['result']) > 0)
        self.assertEqual(data['success'], True)

    def test_200_get_os_stats(self):
        """Test wrong method to GET all browser stats """

        res = self.client().get('/stats/os')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['result']) > 0)
        self.assertEqual(data['success'], True)

    def test_200_get_device_stats(self):
        """Test GET method for all browser stats """

        res = self.client().get('/stats/device')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['result']) > 0)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()