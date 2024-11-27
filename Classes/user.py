from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    Transactions = relationship("UserTransaction",backref="User")



    # @property
    # def first_name(self):
    #     pass
    
    # @first_name.setter
    # def first_name(self, name):
    #     pass

    # @property
    # def last_name(self):
    #     pass
    
    # @last_name.setter
    # def last_name(self,name):
    #     pass
