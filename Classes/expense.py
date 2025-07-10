from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, backref
from database import Base
from transaction import UserTransaction

class Expense(UserTransaction):
    __tablename__ = "Expenses"
    id = Column(Integer,ForeignKey('UserTransactions.id'),primary_key=True)
    date = Column(Date)
    category = Column(String)
    amount = Column(Float)
    storename = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "Expense",
    }

    def __str__(self):
        return f"{self.category} expense spent at {self.storename} for a total of ${self.amount} on {self.date} "