import unittest
from flask import current_app
from web_flask.app import app
from os import getenv
from unittest.mock import Mock, patch

class TestApp(unittest.TestCase):

    def setUp(self):
        """Set up test case environment"""
        self.app = app.test_client()
        self.app.testing = True
        # Manually set TESTING to True
        app.config['TESTING'] = True

    def test_app_exists(self):
        """Test if the app instance exists"""
        with app.app_context():
            self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """Test if the app is in testing mode"""
        self.assertTrue(app.config['TESTING'])

    def test_home_status_code(self):
        """Test if the home route returns a 200 status code"""
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_session_config(self):
        """Test session configuration"""
        self.assertEqual(app.config['SESSION_TYPE'], getenv('SESSION_TYPE'))
        self.assertEqual(app.config['SESSION_FILE_DIR'], getenv('SESSION_FILE_DIR'))
        self.assertEqual(app.config['SESSION_FILE_THRESHOLD'], int(getenv('SESSION_FILE_THRESHOLD')))

    def test_mail_config(self):
        """Test mail configuration"""
        self.assertEqual(app.config['MAIL_SERVER'], getenv('MAIL_SERVER'))
        self.assertEqual(app.config['MAIL_PORT'], int(getenv('MAIL_PORT')))
        self.assertEqual(app.config['MAIL_USE_TLS'], getenv('MAIL_USE_TLS'))
        self.assertEqual(app.config['MAIL_USERNAME'], getenv('MAIL_USERNAME'))
        self.assertEqual(app.config['MAIL_PASSWORD'], getenv('MAIL_PASSWORD'))

    def test_teardown(self):
        """Test if the teardown method closes the session"""
        with self.app:
            with app.app_context():
                with patch('models.storage.close') as mock_close:
                    app.do_teardown_appcontext()
                    mock_close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
