from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from database import Base


class UserTransaction(Base):
    __tablename__ = "UserTransactions"
    id = Column(Integer,primary_key=True, unique=True)
    date = Column(Date)
    category = Column(String)
    amount = Column(Float)
    user_id = Column(Integer, ForeignKey("Users.id"))

