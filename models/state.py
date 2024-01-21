#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")
    else:
        @property
        def cities(self):
            """Getter attribute that returns the list of City instances
            with state_id equal to current State.id"""
            from models import storage
            list_of_cities = []
            retrieved_cities = storage.all(City).values()

            for city in retrieved_cities:
                if city.state_id == self.id:
                    list_of_cities.append(city)
                return list_of_cities
