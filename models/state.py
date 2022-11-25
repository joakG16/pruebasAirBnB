#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base, storage_type
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """ State class/model """
    if storage_type == "db":
        """mapping class to table if DBStorage is specified"""
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        ''' When using backref, you don't need to declare the relationship
        on the second table defined (in this case, cities, from City),
        like back_populates does'''
        cites = relationship("City", backref="state",
                             cascade="all, delete, delete-orphan")

    else:  # filestorage type
        name = ""

        ''' getter attribute "cities" that returns the list of 'City' instances
        with its 'state_id' equals to the current 'State.id' => It will be the
        FileStorage relationship between 'State' and 'City' '''
        @property
        def cities(self):
            ''' method getter '''
            from models.city import City
            return [city for city in models.storage.all(City).values() if
                    city.state_id == self.id]
