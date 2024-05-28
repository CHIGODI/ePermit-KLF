#!/usr/bin/env python3

""" This module contains the mpesa class for storing transaction data """

from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

class Mpesa(BaseModel, Base):
    """ Class for storing mpesa transaction data """
    __tablename__ = 'mpesa'
    TransactionDate = Column(DateTime, nullable=False)
    Amount = Column(Float, nullable=False)
    MpesaReceiptNumber = Column(String(60), nullable=False)
    permit_id = Column(String(60), ForeignKey('permits.id'), nullable=False)
    PhoneNumber = Column(String(20), nullable=False)
    permit = relationship('Permit', backref='mpesa')