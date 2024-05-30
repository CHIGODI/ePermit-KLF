import unittest
from unittest.mock import patch, MagicMock
from web_flask.app import app

class RegisterTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test case environment"""
        self.app = app.test_client()
        self.app.testing = True

    @patch('web_flask.register.g')
    @patch('web_flask.register.storage')
    @patch('web_flask.register.token_required')
    def test_register_page(self, mock_token_required, mock_storage, mock_g):
        """Test register page route"""
        mock_user = MagicMock()
        mock_user.id = 1
        mock_g.current_user = mock_user

        mock_category = MagicMock()
        mock_storage.all.return_value = {'1': mock_category}

        mock_token_required.return_value = lambda func: func

        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'register.html', response.data)
        self.assertIn(b'user_id', response.data)
        self.assertIn(b'categories', response.data)

    @patch('web_flask.register.render_template')
    def test_register_page_no_user_or_categories(self, mock_render_template):
        """Test register page route when there is no user or categories"""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = None

            mock_render_template.return_value = 'dashboard.html'

            response = self.app.get('/register')
            self.assertEqual(response.status_code, 200)
            mock_render_template.assert_called_with('dashboard.html')

    def test_mpesa_express(self):
        """Test mpesa_express route"""
        response = self.app.get('/pay/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'payment.html', response.data)

if __name__ == '__main__':
    unittest.main()
