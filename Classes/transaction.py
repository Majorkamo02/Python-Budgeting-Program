from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, backref
from database import Base


class UserTransaction(Base):
    __tablename__ = "UserTransactions"
    id = Column(Integer,primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    type = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "usertransaction",
        "polymorphic_on": type,
  }
    