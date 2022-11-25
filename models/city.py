#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base, storage_type
from sqlalchemy import Column, String, ForeignKey


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    if storage_type == "db":
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    else:  # filestorage type
        state_id = ""
        name = ""
