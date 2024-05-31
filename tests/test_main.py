import unittest
from unittest.mock import patch, MagicMock
from flask import g
from web_flask.app import app

class MainTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test case environment"""
        self.app = app.test_client()
        self.app.testing = True

    def test_landing_page(self):
        """Test landing page"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'landing_page', response.data)

    @patch('web_flask.main.g')
    @patch('web_flask.main.token_required')
    def test_dashboard(self, mock_token_required, mock_g):
        """Test dashboard route"""
        mock_user = MagicMock()
        mock_user.businesses = []
        mock_g.current_user = mock_user
        mock_token_required.return_value = lambda func: func

        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'services', response.data)

    @patch('web_flask.main.g')
    @patch('web_flask.main.token_required')
    def test_mybusinesses(self, mock_token_required, mock_g):
        """Test mybusinesses route"""
        mock_user = MagicMock()
        mock_user.businesses = []
        mock_g.current_user = mock_user
        mock_token_required.return_value = lambda func: func

        response = self.app.get('/mybusinesses')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'my_businesses', response.data)

    @patch('web_flask.main.g')
    @patch('web_flask.main.token_required')
    def test_myprofile(self, mock_token_required, mock_g):
        """Test myprofile route"""
        mock_user = MagicMock()
        mock_g.current_user = mock_user
        mock_token_required.return_value = lambda func: func

        response = self.app.get('/myprofile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'my_profile', response.data)

    @patch('web_flask.main.g')
    @patch('web_flask.main.token_required')
    def test_mypermits(self, mock_token_required, mock_g):
        """Test mypermits route"""
        mock_user = MagicMock()
        mock_user.permits = []
        mock_g.current_user = mock_user
        mock_token_required.return_value = lambda func: func

        response = self.app.get('/mypermits')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'my_permits', response.data)

    @patch('web_flask.main.g')
    @patch('web_flask.main.token_required')
    def test_renewpermit(self, mock_token_required, mock_g):
        """Test renewpermit route"""
        mock_user = MagicMock()
        mock_g.current_user = mock_user
        mock_token_required.return_value = lambda func: func

        response = self.app.get('/renewpermit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'renewpermit', response.data)

    @patch('web_flask.main.token_required')
    def test_admin_dashboard(self, mock_token_required):
        """Test admin_dashboard route"""
        mock_token_required.return_value = lambda func: func

        response = self.app.get('/admin_dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'admin_dashboard', response.data)

    @patch('web_flask.main.token_required')
    def test_coming_soon(self, mock_token_required):
        """Test coming_soon route"""
        mock_token_required.return_value = lambda func: func

        response = self.app.get('/comingsoon')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'coming_soon', response.data)

if __name__ == '__main__':
    unittest.main()
