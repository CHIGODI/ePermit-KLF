#!/usr/bin/env python3
""" This module contains tests cases for the Mpesa model """

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
from models.mpesa import Mpesa
from datetime import datetime

class TestMpesa(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        # Close the session and drop all tables
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_create_mpesa_transaction(self):
        # Create a new Mpesa transaction
        transaction = Mpesa(
            TransactionDate=datetime.now(),
            Amount=100.50,
            MpesaReceiptNumber="ABC123456",
            permit_id="permit123",
            PhoneNumber="0712345678"
        )
        self.session.add(transaction)
        self.session.commit()

        # Query the database to retrieve the transaction
        result = self.session.query(Mpesa).filter_by(MpesaReceiptNumber="ABC123456").first()

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result.Amount, 100.50)
        self.assertEqual(result.MpesaReceiptNumber, "ABC123456")
        self.assertEqual(result.permit_id, "permit123")
        self.assertEqual(result.PhoneNumber, "0712345678")

if __name__ == '__main__':
    unittest.main()
