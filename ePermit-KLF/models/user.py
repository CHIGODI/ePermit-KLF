#!/usr/bin/python3
""" Contains the User class """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class User(BaseModel, Base, UserMixin):
    """ Class for user instances """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=(False))
    first_name = Column(String(60), nullable=True)
    last_name = Column(String(60), nullable=True)
    gender = Column(String(20), nullable=True)
    designation = Column(String(60), nullable=True)
    ID_number = Column(Integer, nullable=True)
    phone_number = Column(Integer, nullable=True)
    businesses = relationship("Business",
                              backref="user",
                              cascade="all, delete-orphan")
