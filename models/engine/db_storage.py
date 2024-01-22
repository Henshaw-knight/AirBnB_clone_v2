#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
import os
from sqlalchemy import create_engine
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage():
    """The class for handling db storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the SQL db storage"""
        username = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        database_name = os.getenv("HBNB_MYSQL_DB")
        env = os.getenv("HBNB_ENV")

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
                               username, password, host, database_name),
                               pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of objects"""
        class_list = [State, City, User, Place, Amenity, Review]
        object_dict = {}
        if cls is not None:
            if cls in class_list:
                for row in self.__session.query(cls).all():
                    key = "{}.{}".format(row.__class__.__name__, row.id)
                    object_dict[key] = row
        else:
            for class_name in class_list:
                for row in self.__session.query(class_name).all():
                    key = "{}.{}".format(row.__class__.__name__, row.id)
                    object_dict[key] = row

        return object_dict

    def new(self, obj):
        """Adds obj (the object) to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the curren database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes `obj` from the current database session if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Loads tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
