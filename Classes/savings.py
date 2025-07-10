from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, backref
from database import Base
from transaction import UserTransaction

class Save(UserTransaction):
    __tablename__ = "Savings"
    id = Column(Integer,ForeignKey('UserTransactions.id'),primary_key=True)
    date = Column(Date)
    amount = Column(Float)
    account_name = Column(String)
    account_type = Column(String)


    __mapper_args__ = {
        "polymorphic_identity": "Saving",
    }

    def __str__(self):
        return f"${self.amount} saved in account {self.account_name} on {self.date}"