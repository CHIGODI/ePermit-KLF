#!/usr/bin/env python3
""" Contains the Business class """

from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, Float, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship


class Business(BaseModel, Base):
    """ Class for business instances """

    __tablename__ = 'businesses'
    name = Column(String(64), nullable=False)
    entity_origin = Column(String(20), nullable=False)
    Certificate_of_Registration_No = Column(Integer, nullable=False)
    KRA_pin = Column(String(60), nullable=False)
    vat_no = Column(Integer, nullable=True)
    po_box = Column(Integer, nullable=False)
    postal_code = Column(Integer, nullable=False)
    business_telephone = Column(String(20), nullable=False)
    business_telephone_two = Column(String(20), nullable=True)
    business_email = Column(String(64), nullable=True)
    sub_county = Column(String(64), nullable=False)
    ward = Column(String(64), nullable=False)
    physical_address = Column(String(128), nullable=False)
    plot_no = Column(Integer, nullable=True)
    activity_code_description = Column(String(256), nullable=False)
    detailed_description = Column(String(256), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    number_of_employees = Column(Integer, nullable=False)

    #will be provided backend logic
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    category_id = Column(String(60), ForeignKey('categories.id'), nullable=False)
    verified = Column(Boolean, nullable=True, default=False)