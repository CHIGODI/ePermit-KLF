#!/usr/bin/python3
""" Contains the Category class """

from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, Float, ForeignKey
from sqlalchemy.orm import relationship


class Category(BaseModel, Base):
    """" Class for category instances """
    __tablename__ = 'categories'
    category_name = Column(String(60), nullable=False)
    description = Column(String(256), nullable=True)
    fee = Column(Float, nullable=False)