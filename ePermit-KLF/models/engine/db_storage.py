#!/usr/bin/python3
""" Contains the DBStorage class """

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv 



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
        if cls is None:
            return self.__session.query().all()
        return self.__session.query(cls).all()
    
    def get(self, cls, id):
        """ retrieves an object from the database """
        if cls is None or id is None:
            return None
        return self.__session.query(cls).get(id)
        
    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session
        
    def close(self):
        """ closes the session """
        self.__session.remove()