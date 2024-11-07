from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import random
from .transaction import Transaction

Base = declarative_base()



class User(Base):
    __tablename__ = "user_table"
    _account_number = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique = True)

    Transaction = relationship("transaction_table", back_populates="user_table")

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.account_number = User.generate_random_id()    

    @property
    def account_number(self):
        return self._account_number
    
    @account_number.setter
    def account_number(self, new_id):
        self._account_number = new_id 
        session.add(self)
        session.commit()

    @property
    def first_name(self):
        return self.first_name
    
    @first_name.setter
    def first_name(self, name):
        self.first_name = name 
        session.add(self)
        session.commit()

    @property
    def last_name(self):
        return self.last_name
    
    @last_name.setter
    def last_name(self, name):
        self.last_name = name 
        session.add(self)
        session.commit()

    def generate_random_id():
        while True:
            new_account_number = random.randint(1000,9999)
            if not session.query(User).filter_by(_account_number=new_account_number).first():
                return new_account_number
        
            

engine = create_engine("sqlite:///C:/Users\Cameron\Desktop\School\Fall 2024\Object Oriented Programming\Final Project\Data_Base/test.db")
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()