import unittest
from datetime import datetime, timedelta
from web_flask.reused_functions import time_diff_from_now, generate_verification_code

class TestReusedFunctions(unittest.TestCase):

    def test_time_diff_from_now(self):
        """Test the time_diff_from_now function"""
        # Create a timestamp 5 minutes ago
        past_timestamp = (datetime.utcnow() - timedelta(minutes=5)).isoformat()

        # Calculate time difference
        diff = time_diff_from_now(past_timestamp)

        # Assert the difference is around 300 seconds (5 minutes)
        self.assertAlmostEqual(diff, 300, delta=2)  # Allowing a small delta for execution time

    def test_generate_verification_code(self):
        """Test the generate_verification_code function"""
        # Generate a code
        code = generate_verification_code()

        # Assert the code is of the correct length
        self.assertEqual(len(code), 6)

        # Assert the code contains only uppercase letters and digits
        self.assertTrue(all(c.isdigit() or c.isupper() for c in code))

        # Test with a different length
        code = generate_verification_code(length=8)
        self.assertEqual(len(code), 8)

if __name__ == '__main__':
    unittest.main()
