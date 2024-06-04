import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
from models.permit import Permit

class TestPermit(unittest.TestCase):

    def setUp(self):
        """Set up test case environment"""
        self.permit = Permit(
            is_valid=True,
            business_id="test_business_id",
            user_id="test_user_id"
        )

    def test_initialization(self):
        """Test that a Permit instance is correctly initialized"""
        self.assertEqual(self.permit.is_valid, True)
        self.assertEqual(self.permit.business_id, "test_business_id")
        self.assertEqual(self.permit.user_id, "test_user_id")
        self.assertTrue(self.permit.permit_number.startswith(datetime.utcnow().strftime("%Y%m%d")))
        self.assertEqual(len(self.permit.permit_number.split('-')[-1]), 6)

    def test_str_method(self):
        """Test the __str__ method"""
        permit_str = str(self.permit)
        expected_str = "[Permit] ({}) {}".format(self.permit.id, self.permit.__dict__)
        self.assertEqual(permit_str, expected_str)

    def test_to_dict_method(self):
        """Test the to_dict method"""
        permit_dict = self.permit.to_dict()
        self.assertEqual(permit_dict["__class__"], "Permit")
        self.assertEqual(permit_dict["permit_number"], self.permit.permit_number)
        self.assertEqual(permit_dict["is_valid"], True)
        self.assertEqual(permit_dict["business_id"], "test_business_id")
        self.assertEqual(permit_dict["user_id"], "test_user_id")

    def test_generate_permit_number(self):
        """Test the generate_permit_number method"""
        permit_number = self.permit.generate_permit_number()
        self.assertTrue(permit_number.startswith(datetime.utcnow().strftime("%Y%m%d")))
        self.assertEqual(len(permit_number.split('-')[-1]), 6)

    def test_check_validity(self):
        """Test the check_validity method"""
        self.permit.created_at = datetime.utcnow() - timedelta(days=364)
        self.assertTrue(self.permit.check_validity())

        self.permit.created_at = datetime.utcnow() - timedelta(days=366)
        self.assertFalse(self.permit.check_validity())

    @patch('models.storage')
    def test_save_method(self, mock_storage):
        """Test the save method"""
        old_updated_at = self.permit.updated_at
        self.permit.save()
        self.assertNotEqual(self.permit.updated_at, old_updated_at)
        mock_storage.new.assert_called_once_with(self.permit)
        mock_storage.save.assert_called_once()

    @patch('models.storage')
    def test_delete_method(self, mock_storage):
        """Test the delete method"""
        self.permit.delete()
        mock_storage.delete.assert_called_once_with(self.permit)

if __name__ == '__main__':
    unittest.main()
