import sqlalchemy
from user import User
from database import session
from transaction import UserTransaction
from datetime import datetime, date

class data_management(User):
    def create_new_user():        
        first = input("What is your first name? ")
        last = input("What is your last name? ")
        while True:    
            email = input("What is your email? ")
            
            try:
                new_user = User(first_name=first, last_name=last, email=email)
                new_transaction = UserTransaction(date=datetime(2024,1,1), category="test", amount=0.0 )
                new_user.Transactions.append(new_transaction)
                session.add_all([new_user,new_transaction])
                session.commit()
                print(f"User {new_user.first_name} {new_user.last_name} Created with account number: {new_user.id}")
                return new_user
                break
            except sqlalchemy.exc.IntegrityError:
                session.rollback()
                print("Error! Please try another email address")


    def csv_commit(file):
        pass

    def close_account():
        pass

    def create_expense():
        pass
