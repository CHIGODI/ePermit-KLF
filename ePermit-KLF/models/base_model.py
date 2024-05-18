#!/usr/bin/python3  
""" Contains common attributes inherited by all classes """

from datetime import datetime, timezone
import uuid
from sqlalchemy.ext.declarative import declarative_base
import models
# from flask_sqlalchemy import SQLAlchemy


# db = SQLAlchemy()

Base = declarative_base()
# Used this in the to_dict method
time = "%Y-%m-%dT%H:%M:%S.%f"

class BaseModel:
    """ Base class for all other classes """
    from sqlalchemy import Column, DateTime, String
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    id = Column(String(60), unique=True, primary_key=True,  nullable=False)

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
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
