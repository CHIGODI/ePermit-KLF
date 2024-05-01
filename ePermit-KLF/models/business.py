#!/usr/bin/python3
""" Contains the Business class """

from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, Float, ForeignKey
from sqlalchemy.orm import relationship


class Business(BaseModel, Base):
    """ Class for business instances """
    
    __tablename__ = 'businesses'
    name = Column(String(64), nullable=False)
    description = Column(String(256), nullable=True)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    category_id = Column(String(60), ForeignKey('categories.id'), nullable=False)
    Latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String(128), nullable=False)
    KRA_pin = Column(String(60), nullable=False)
