#!/usr/bin/python3  
""" Contains common attributes inherited by all classes """

from datetime import datetime, timezone
import uuid
from sqlalchemy.ext.declarative import declarative_base
import models

Base = declarative_base()


class BaseModel:
    """ Base class for all other classes """
    from sqlalchemy import Column, DateTime, String
    created_at = Column(DateTime,
                        nullable=False,
                        default=datetime.now(timezone.utc))
    updated_at = Column(DateTime,
                        nullable=False,
                        default=datetime.now(timezone.utc))
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    def __init__(self, *args, **kwargs):
        """ Initializes the base class """
        if kwargs:
            kwargs['created_at'] = kwargs.get('created_at', datetime.now().isoformat())
            kwargs['updated_at'] = kwargs.get('updated_at', datetime.now().isoformat())
            kwargs['id'] = kwargs.get('id', str(uuid.uuid4()))
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != '__class__' and key != '_sa_instance_state':
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            
    def __str__(self):
        """ Returns a string representation of the class """
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    
    def save(self):
        """ Updates the updated_at attribute with the current datetime """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()
        
    def to_dict(self):
        """ Returns a dictionary representation of the class """
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        return new_dict