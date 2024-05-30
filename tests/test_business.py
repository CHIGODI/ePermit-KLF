import unittest
from unittest.mock import patch
from datetime import datetime
from models.business import Business

class TestBusiness(unittest.TestCase):

    def setUp(self):
        """Set up test case environment"""
        self.business = Business(
            business_name="Test Business",
            entity_origin="Kenya",
            Certificate_of_Registration_No=123456,
            KRA_pin="A1234567890",
            vat_no="V123456789012345",
            po_box=12345,
            postal_code=67890,
            business_telephone="0712345678",
            business_telephone_two="0723456789",
            business_email="test@example.com",
            sub_county="Nairobi",
            ward="Westlands",
            physical_address="123 Test Street",
            plot_no="123",
            category="test_category_id",
            detailed_description="A detailed description of the business.",
            number_of_employees=10,
            latitude=-1.286389,
            longitude=36.817223,
            owner="test_owner_id",
            verified=True
        )

    def test_initialization(self):
        """Test that a Business instance is correctly initialized"""
        self.assertEqual(self.business.business_name, "Test Business")
        self.assertEqual(self.business.entity_origin, "Kenya")
        self.assertEqual(self.business.Certificate_of_Registration_No, 123456)
        self.assertEqual(self.business.KRA_pin, "A1234567890")
        self.assertEqual(self.business.vat_no, "V123456789012345")
        self.assertEqual(self.business.po_box, 12345)
        self.assertEqual(self.business.postal_code, 67890)
        self.assertEqual(self.business.business_telephone, "0712345678")
        self.assertEqual(self.business.business_telephone_two, "0723456789")
        self.assertEqual(self.business.business_email, "test@example.com")
        self.assertEqual(self.business.sub_county, "Nairobi")
        self.assertEqual(self.business.ward, "Westlands")
        self.assertEqual(self.business.physical_address, "123 Test Street")
        self.assertEqual(self.business.plot_no, "123")
        self.assertEqual(self.business.category, "test_category_id")
        self.assertEqual(self.business.detailed_description, "A detailed description of the business.")
        self.assertEqual(self.business.number_of_employees, 10)
        self.assertEqual(self.business.latitude, -1.286389)
        self.assertEqual(self.business.longitude, 36.817223)
        self.assertEqual(self.business.owner, "test_owner_id")
        self.assertTrue(self.business.verified)

    def test_str_method(self):
        """Test the __str__ method"""
        business_str = str(self.business)
        expected_str = "[Business] ({}) {}".format(self.business.id, self.business.__dict__)
        self.assertEqual(business_str, expected_str)

    def test_to_dict_method(self):
        """Test the to_dict method"""
        business_dict = self.business.to_dict()
        self.assertEqual(business_dict["__class__"], "Business")
        self.assertEqual(business_dict["business_name"], "Test Business")
        self.assertEqual(business_dict["entity_origin"], "Kenya")
        self.assertEqual(business_dict["Certificate_of_Registration_No"], 123456)
        self.assertEqual(business_dict["KRA_pin"], "A1234567890")
        self.assertEqual(business_dict["vat_no"], "V123456789012345")
        self.assertEqual(business_dict["po_box"], 12345)
        self.assertEqual(business_dict["postal_code"], 67890)
        self.assertEqual(business_dict["business_telephone"], "0712345678")
        self.assertEqual(business_dict["business_telephone_two"], "0723456789")
        self.assertEqual(business_dict["business_email"], "test@example.com")
        self.assertEqual(business_dict["sub_county"], "Nairobi")
        self.assertEqual(business_dict["ward"], "Westlands")
        self.assertEqual(business_dict["physical_address"], "123 Test Street")
        self.assertEqual(business_dict["plot_no"], "123")
        self.assertEqual(business_dict["category"], "test_category_id")
        self.assertEqual(business_dict["detailed_description"], "A detailed description of the business.")
        self.assertEqual(business_dict["number_of_employees"], 10)
        self.assertEqual(business_dict["latitude"], -1.286389)
        self.assertEqual(business_dict["longitude"], 36.817223)
        self.assertEqual(business_dict["owner"], "test_owner_id")
        self.assertTrue(business_dict["verified"])

    @patch('models.storage')
    def test_save_method(self, mock_storage):
        """Test the save method"""
        old_updated_at = self.business.updated_at
        self.business.save()
        self.assertNotEqual(self.business.updated_at, old_updated_at)
        mock_storage.new.assert_called_once_with(self.business)
        mock_storage.save.assert_called_once()

    @patch('models.storage')
    def test_delete_method(self, mock_storage):
        """Test the delete method"""
        self.business.delete()
        mock_storage.delete.assert_called_once_with(self.business)

if __name__ == '__main__':
    unittest.main()
