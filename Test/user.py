from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base


class User():
    def __init__(self, name, gmail):
        self._name = name
        self._gmail = gmail

    @property
    def name(self,):
        return self._self

    @name.setter
    def name(self, name):
        self._name = name

