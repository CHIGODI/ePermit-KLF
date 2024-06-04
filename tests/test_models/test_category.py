import unittest
from unittest.mock import patch
from datetime import datetime
from models.category import Category

class TestCategory(unittest.TestCase):

    def setUp(self):
        """Set up test case environment"""
        self.category = Category(
            activity_code="A1234",
            category_name="Test Category",
            description="This is a test category",
            fee=100.0,
            fire_fee=50.0
        )

    def test_initialization(self):
        """Test that a Category instance is correctly initialized"""
        self.assertEqual(self.category.activity_code, "A1234")
        self.assertEqual(self.category.category_name, "Test Category")
        self.assertEqual(self.category.description, "This is a test category")
        self.assertEqual(self.category.fee, 100.0)
        self.assertEqual(self.category.fire_fee, 50.0)

    def test_str_method(self):
        """Test the __str__ method"""
        category_str = str(self.category)
        expected_str = "[Category] ({}) {}".format(self.category.id, self.category.__dict__)
        self.assertEqual(category_str, expected_str)

    def test_to_dict_method(self):
        """Test the to_dict method"""
        category_dict = self.category.to_dict()
        self.assertEqual(category_dict["__class__"], "Category")
        self.assertEqual(category_dict["activity_code"], "A1234")
        self.assertEqual(category_dict["category_name"], "Test Category")
        self.assertEqual(category_dict["description"], "This is a test category")
        self.assertEqual(category_dict["fee"], 100.0)
        self.assertEqual(category_dict["fire_fee"], 50.0)

    @patch('models.storage')
    def test_save_method(self, mock_storage):
        """Test the save method"""
        old_updated_at = self.category.updated_at
        self.category.save()
        self.assertNotEqual(self.category.updated_at, old_updated_at)
        mock_storage.new.assert_called_once_with(self.category)
        mock_storage.save.assert_called_once()

    @patch('models.storage')
    def test_delete_method(self, mock_storage):
        """Test the delete method"""
        self.category.delete()
        mock_storage.delete.assert_called_once_with(self.category)

if __name__ == '__main__':
    unittest.main()
