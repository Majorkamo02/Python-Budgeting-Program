from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    
    Transaction = relationship("transaction", back_populates="user")


    def __repr__(self):
        return f"Name : {self.firstname} {self.lastname} [{self.email}]"


class Transaction(Base):
    __tablename__ = "transaction"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    expense = Column(Float)
    income = Column(Float)
    savings = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))  
    

    user = relationship("User", back_populates="transaction")


    def __repr__(self):
        return f"expense={self.expense}, income={self.income}, savings={self.savings}"



engine = create_engine("sqlite:///test.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


new_user = User(id = 1, firstname="Cameron", lastname="Jolly", email="cameron.l.jolly@gmail.com")
session.add(new_user)
session.commit()

new_finance = Transaction(expense=200.0, income=1500.0, savings=100.0, user_id=new_user.id)
session.add(new_finance)
session.commit()

new_finance = Transaction(expense=899.0, income=900.0, savings=1.0, user_id=new_user.id)
session.add(new_finance)
session.commit()

user = session.query(User).filter_by(id=1).first()

print(user.Transaction)

finance_record = session.query(Transaction).filter_by(id=1).first()
print(finance_record.user)
