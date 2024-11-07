from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transaction_table"
    transaction_id = Column("Transaction Id", Integer, primary_key=True)
    date = Column("Date", String)
    amount = Column("Amount in $", Float)

    User = relationship("user_table", back_populates=("transaction_table"))
