import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
import jwt
from jwt.algorithms import encode
from werkzeug.security import generate_password_hash
from web_flask.app import app  # Import your create_app function
from models.user import User

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()  # Use create_app to get the Flask app instance
        self.app.testing = True
        self.secret_key = 'test_secret_key'
        self.email = 'test@example.com'
        self.password = 'password123'
        self.user = User(id=1, email=self.email, password=generate_password_hash(self.password))
        self.token = jwt.encode({'id': self.user.id, 'exp': datetime.utcnow() + timedelta(minutes=30)}, self.secret_key, algorithm='HS256')

    @patch('web_flask.auth.storage.get_user_by_email')
    @patch('web_flask.auth.check_password_hash')
    def test_login(self, mock_check_password, mock_get_user):
        mock_get_user.return_value = self.user
        mock_check_password.return_value = True
        
        response = self.app.post('/login/', data={'email': self.email, 'password': self.password})
        self.assertEqual(response.status_code, 302)
        self.assertIn('x-access-token', response.headers['Set-Cookie'])

    @patch('web_flask.auth.storage.get_user_by_email')
    @patch('web_flask.auth.generate_password_hash')
    def test_signup(self, mock_generate_password, mock_get_user):
        mock_get_user.return_value = None
        mock_generate_password.return_value = generate_password_hash(self.password)
        
        with self.app.session_transaction() as sess:
            sess['verification_data'] = {
                'email': self.email,
                'password': generate_password_hash(self.password),
                'verification_code': '123456',
                'timestamp': datetime.utcnow().isoformat()
            }

        response = self.app.post('/signup/', data={
            'email': self.email,
            'password': self.password,
            'confirm_password': self.password
        })
        self.assertEqual(response.status_code, 302)

    @patch('web_flask.auth.storage.get_user_by_email')
    def test_forgot_password(self, mock_get_user):
        mock_get_user.return_value = self.user
        
        response = self.app.post('/forgot_password/', data={'email': self.email})
        self.assertEqual(response.status_code, 302)
        self.assertIn('Check email', response.get_data(as_text=True))

    @patch('web_flask.auth.jwt.decode')
    @patch('web_flask.auth.generate_password_hash')
    def test_reset_password(self, mock_generate_password, mock_jwt_decode):
        mock_jwt_decode.return_value = {'id': self.user.id}
        mock_generate_password.return_value = generate_password_hash(self.password)
        
        with self.app.session_transaction() as sess:
            sess['user'] = self.user
        
        response = self.app.post(f'/reset_password/{self.token}', data={
            'new_password': self.password,
            'confirm_new_password': self.password
        })
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        response = self.app.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('x-access-token', response.headers.get('Set-Cookie', ''))

if __name__ == '__main__':
    unittest.main()
