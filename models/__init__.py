#!/usr/bin/python3

""" creates storage object that is used to interact with DB """
from models.engine.db_storage import DBStorage

storage = DBStorage()
storage.reload()