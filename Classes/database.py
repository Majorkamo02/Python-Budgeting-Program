from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

class Base(DeclarativeBase):
    pass

engine = create_engine(r"sqlite:///C:/Users\Cameron\Desktop\School\Fall 2024\Object Oriented Programming\Final Project\Data_Base/Customer Database.db")

Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)