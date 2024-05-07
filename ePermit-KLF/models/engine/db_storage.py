#!/usr/bin/python3
""" Contains the DBStorage class """

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv
from models.user import User
from models.business import Business
from models.category import Category


classes = {"User": User, "Business": Business, "Category": Category}


class DBStorage:
    """ storage class for database """
    __session = None
    __engine = None
    
    def __init__(self):
        """ initializes the DBStorage class """
        EPERMIT_MYSQL_USER = getenv('EPERMIT_MYSQL_USER')
        EPERMIT_MYSQL_PWD = getenv('EPERMIT_MYSQL_PWD')
        EPERMIT_MYSQL_HOST = getenv('EPERMIT_MYSQL_HOST')
        EPERMIT_MYSQL_DB = getenv('EPERMIT_MYSQL_DB')
        EPERMIT_ENV = getenv('EPERMIT_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(EPERMIT_MYSQL_USER,
                                             EPERMIT_MYSQL_PWD,
                                             EPERMIT_MYSQL_HOST,
                                             EPERMIT_MYSQL_DB))
        
        if EPERMIT_ENV == 'test':
            Base.metadata.drop_all(self.__engine)
            
    def new(self, obj):
        """ saves an object to the database """
        self.__session.add(obj)
            
    def save(self):
        """ commits all changes to the database """
        self.__session.commit()

    def all(self, cls=None):
        """ retrieves all objects from the database """
        new_dict = {}
        for clas in classes:
            if cls is None or cls is classes[clas] or cls is clas:
                objects = self.__session.query(classes[clas]).all()
                for obj in objects:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    new_dict[key] = obj
        return new_dict

    
    def get(self, cls, id):
        """ retrieves an object from the database """
        if cls is None or id is None:
            return None
        return self.__session.query(cls).get(id)

    def delete(self, obj=None):
        """ deletes an object from the current database """
        if obj is not None:
            self.__session.delete(obj)
        
    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session
    
    def count(self, cls=None):
        """ counts the number of objects in the database """
        if cls is None:
            cls_count = 0
            for i in self.all().values():
                cls_count += 1
            return cls_count
        else:
            cls_count = 0
            for i in self.all(cls).values():
                cls_count += 1
            return cls_count

    def close(self):
        """ closes the session """
        self.__session.remove()
