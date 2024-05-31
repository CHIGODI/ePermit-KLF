import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):

    def setUp(self):
        """Set up test case environment"""
        self.model = BaseModel()

    def test_initialization(self):
        """Test that an instance is correctly initialized"""
        self.assertIsNotNone(self.model.id)
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model.updated_at, datetime)
        self.assertAlmostEqual(self.model.created_at, self.model.updated_at, delta=timedelta(seconds=1))

    def test_str_method(self):
        """Test the __str__ method"""
        model_str = str(self.model)
        expected_str = "[BaseModel] ({}) {}".format(self.model.id, self.model.__dict__)
        self.assertEqual(model_str, expected_str)

    @patch('models.storage')
    def test_save_method(self, mock_storage):
        """Test the save method"""
        old_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(self.model.updated_at, old_updated_at)
        mock_storage.new.assert_called_once_with(self.model)
        mock_storage.save.assert_called_once()

    def test_to_dict_method(self):
        """Test the to_dict method"""
        model_dict = self.model.to_dict()
        self.assertEqual(model_dict["__class__"], "BaseModel")
        self.assertEqual(model_dict["id"], self.model.id)
        self.assertEqual(model_dict["created_at"], self.model.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f"))
        self.assertEqual(model_dict["updated_at"], self.model.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f"))
        self.assertNotIn("_sa_instance_state", model_dict)

    @patch('models.storage')
    def test_delete_method(self, mock_storage):
        """Test the delete method"""
        self.model.delete()
        mock_storage.delete.assert_called_once_with(self.model)

if __name__ == '__main__':
    unittest.main()
