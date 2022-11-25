#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os


switch = os.environ.get("HBNB_TYPE_STORAGE")  # can be "db", for example

if switch == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
