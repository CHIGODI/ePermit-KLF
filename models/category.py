#!/usr/bin/env python3
""" Contains the Category class """

from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, Float


class Category(BaseModel, Base):
    """" Class for category instances """
    __tablename__ = 'categories'
    activity_code = Column(String(8), nullable=False)
    category_name = Column(String(128), nullable=False)
    description = Column(String(256), nullable=True)
    fee = Column(Float, nullable=False)
    fire_fee = Column(Float, nullable=False)