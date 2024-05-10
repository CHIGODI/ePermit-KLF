#!/usr/bin/python3
""" Contains the Business class """

from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Business(BaseModel, Base):
    """ Class for business instances """
    
    __tablename__ = 'businesses'
    name = Column(String(64), nullable=False)
    entity_origin = Column(String(20), nullable=False)
    vat_no = Column(Integer, nullable=True)
    po_box = Column(Integer, nullable=False)
    postal_code = Column(Integer, nullable=False)
    business_telephone = Column(Integer, nullable=False)
    activity_description = Column(String(256), nullable=True)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    category_id = Column(String(60), ForeignKey('categories.id'), nullable=False)
    Latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    sub_county = Column(String, nullable=False)
    ward = Column(String, nullable=False)
    plot_number=Column(String(60), nullable=True)
    KRA_pin = Column(String(60), nullable=False)
    
    
    
