from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, backref
from database import Base
from transaction import UserTransaction

class Income(UserTransaction):
    __tablename__ = "Incomes"
    id = Column(Integer,ForeignKey('UserTransactions.id'),primary_key=True)
    date = Column(Date)
    amount = Column(Float)
    employer = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "Income",
    }

    def __str__(self):
        return f"Income amount ${self.amount} received on {self.date} from {self.employer}"