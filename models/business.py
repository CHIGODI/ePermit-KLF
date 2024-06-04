#!/usr/bin/env python3
""" Contains the Business class """

from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, Float, ForeignKey, Integer, Boolean


class Business(BaseModel, Base):
    """ Class for business instances """

    __tablename__ = 'businesses'
    business_name = Column(String(64), nullable=False)
    entity_origin = Column(String(20), nullable=False)
    Certificate_of_Registration_No = Column(Integer, nullable=False)
    KRA_pin = Column(String(11), nullable=False)
    vat_no = Column(String(24), nullable=True)
    po_box = Column(Integer, nullable=False)
    postal_code = Column(Integer, nullable=False)
    business_telephone = Column(String(20), nullable=False)
    business_telephone_two = Column(String(20), nullable=True)
    business_email = Column(String(64), nullable=True)
    sub_county = Column(String(64), nullable=False)
    ward = Column(String(64), nullable=False)
    physical_address = Column(String(128), nullable=False)
    plot_no = Column(String(24), nullable=True)
    category = Column(String(60), ForeignKey('categories.id'), nullable=False)
    detailed_description = Column(String(256), nullable=True)
    number_of_employees = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    owner = Column(String(60), ForeignKey('users.id'), nullable=False)
    verified = Column(Boolean, nullable=True, default=False)
    status = Column(String(20), nullable=True, default='Pending')
