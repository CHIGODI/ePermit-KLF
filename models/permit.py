#!/usr/bin/env python3
""" This module contains permit class """

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from models.base_model import BaseModel, Base
import uuid

class Permit(BaseModel, Base):
    """Class for permit instances"""
    __tablename__ = 'permits'
    permit_number = Column(String(60), nullable=False, unique=True)
    is_valid = Column(Boolean, default=True, nullable=False)
    business_id = Column(String(60), ForeignKey('businesses.id'), nullable=True)

    def __init__(self, *args, **kwargs):
        """ Override the default init method to set the permit number"""
        super().__init__(*args, **kwargs)
        if not self.permit_number:
            self.permit_number = self.generate_permit_number()

    def generate_permit_number(self):
        """Generate a permit number based on the current date and a random UUID"""
        current_date = datetime.utcnow().strftime("%Y%m%d")
        random_component = uuid.uuid4().hex[:6].upper()
        return f"{current_date}-{random_component}"

    def check_validity(self):
        """Check if the permit is still valid"""
        if datetime.utcnow() > self.created_at + timedelta(days=365):
            self.is_valid = False
        return self.is_valid
