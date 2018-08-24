#!/usr/bin/python3
'''
    Implementation of the User class which inherits from BaseModel
'''
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from hashlib import md5
from os import getenv


class User(BaseModel, Base):
    '''
        Definition of the User class
    '''
    __tablename__ = "users"
    if getenv("HBNB_TYPE_STORAGE", "fs") == "db":
        email = Column(String(128), nullable=False)
        __password = Column("password", String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user",
                              cascade="all, delete, delete-orphan")
        reviews = relationship("Review", backref="user",
                               cascade="all, delete, delete-orphan")
    else:
        email = ""
        __password = ""
        first_name = ""
        last_name = ""

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password=None):
        if password != None:
            self.__password = md5(password.encode()).hexdigest()
