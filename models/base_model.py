#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, DateTime
import os


storage_type = os.environ.get("HBNB_TYPE_STORAGE")

if storage_type == "db":
    Base = declarative_base()
else:
    class Base:
        pass

class BaseModel:
    """A base class for all hbnb models"""
    if storage_type == "db":
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
        updated_at = Column(DateTime, default=datetime.now(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            
        else:
            if 'id' not in kwargs:
                kwargs['id'] = str(uuid.uuid4())

            if 'created at' not in kwargs:
                kwargs['created_at'] = datetime.now()  # instance created NOW
            elif not isinstance('created_at', datetime):
                ''' if the format provided from argu. is not the correct '''
                kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                         '%Y-%m-%dT%H:%M:%S.%f')
            if 'updated_at' not in kwargs:
                kwargs['updated_at'] = datetime.now()
            elif not isinstance('updated_at', datetime):
                kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                         '%Y-%m-%dT%H:%M:%S.%f')
            for key, value in kwargs.items():
                ''' The setattr() function sets the value of the attr.
                of an object. Example, if 'name': "Califronia" is passed '''
                setattr(self, key, value)

            if storage_type != "db":  # requisite for filestorage
                del kwargs['__class__']        

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        try:
            del dictionary['_sa_instance_state']
        except KeyError:  # key not found, doesn't exists
            pass

        return dictionary

    def delete(self):
        from models import storage
        storage.delete(self)  # delete method from file_storage.py
