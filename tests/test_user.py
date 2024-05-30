import unittest
from unittest.mock import patch
from models.user import User  # Adjust the import according to your module structure

class TestUser(unittest.TestCase):

    def setUp(self):
        """Set up test case environment"""
        self.user = User(
            email="test@example.com",
            password="securepassword",
            first_name="John",
            last_name="Doe",
            ID_number=12345678,
            gender="Male",
            designation="Manager",
            phone_number="123-456-7890",
            role="admin"
        )

    def test_initialization(self):
        """Test that a User instance is correctly initialized"""
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.password, "securepassword")
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.ID_number, 12345678)
        self.assertEqual(self.user.gender, "Male")
        self.assertEqual(self.user.designation, "Manager")
        self.assertEqual(self.user.phone_number, "123-456-7890")
        self.assertEqual(self.user.role, "admin")

    def test_str_method(self):
        """Test the __str__ method"""
        user_str = str(self.user)
        expected_str = "[User] ({}) {}".format(self.user.id, self.user.__dict__)
        self.assertEqual(user_str, expected_str)

    def test_to_dict_method(self):
        """Test the to_dict method"""
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict["__class__"], "User")
        self.assertEqual(user_dict["email"], "test@example.com")
        self.assertEqual(user_dict["first_name"], "John")
        self.assertEqual(user_dict["last_name"], "Doe")
        self.assertEqual(user_dict["ID_number"], 12345678)
        self.assertEqual(user_dict["gender"], "Male")
        self.assertEqual(user_dict["designation"], "Manager")
        self.assertEqual(user_dict["phone_number"], "123-456-7890")
        self.assertEqual(user_dict["role"], "admin")

    def test_has_role(self):
        """Test the has_role method"""
        self.assertTrue(self.user.has_role("admin"))
        self.assertFalse(self.user.has_role("user"))

    @patch('models.storage')
    def test_save_method(self, mock_storage):
        """Test the save method"""
        old_updated_at = self.user.updated_at
        self.user.save()
        self.assertNotEqual(self.user.updated_at, old_updated_at)
        mock_storage.new.assert_called_once_with(self.user)
        mock_storage.save.assert_called_once()

    @patch('models.storage')
    def test_delete_method(self, mock_storage):
        """Test the delete method"""
        self.user.delete()
        mock_storage.delete.assert_called_once_with(self.user)

if __name__ == '__main__':
    unittest.main()
