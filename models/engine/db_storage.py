#!/usr/bin/python3
""" DataBase type storage class """
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
USER = os.environ.get('HBNB_MYSQL_USER')  # enviroment variables
PWD = os.environ.get('HBNB_MYSQL_PWD')
HOST = os.environ.get('HBNB_MYSQL_HOST')
DB = os.environ.get('HBNB_MYSQL_DB')
ENV = os.environ.get('HBNB_ENV')

class DBStorage:
    ''' database class '''
    __engine = None
    __session = None

    classes = {
        'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            USER, PWD, HOST, DB), pool_pre_ping=True)
        if ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Makes a query on our DataBase and return all objects,
        depending if class is given, return objects of its type only"""
        obj_dict = {}
        if cls is not None:  # class is provided
            for obj in self.__session.query(cls).all():
                obj_dict[f"{cls}.{obj.id}"] = obj
        else:
            for clas in DBStorage.classes.values(): # iter. through every class
                for obj in self.__session.query(clas).all():  
                    # query every class available in the current database
                    obj_dict[f"{type(obj).__name__}.{obj.id}"] = obj
                    # key = <class-name>.<object-id>
                    # value = object    
        return obj_dict


    def save(self):
        ''' commit all changes of the current database session '''
        self.__session.commit()

    def new(self, obj):
        """ Add the obj to the current db session """
        self.__session.add(obj)
        self.save()

    def delete(self, obj=None):
        ''' delete from the current database session obj if not None '''
        if obj is not None:
            self.__session.delete(obj)
            self.save()
    
    def reload(self):
        ''' create all tables in the database and
        creates the current database session'''
        Base.metadata.create_all(self.__engine)

        session = sessionmaker(self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
    
        self.__session = Session()
