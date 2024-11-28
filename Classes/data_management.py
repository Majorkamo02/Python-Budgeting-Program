import sqlalchemy
from user import User
from database import session
from transaction import UserTransaction
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash


class data_management(User):
    def create_new_user():        
        first = input("What is your first name? ")
        last = input("What is your last name? ")
        # loop1=True
        while True:    
            email = input("What is your email? ")
            
            try:
                UserTransaction()
                new_user = User(first_name=first, last_name=last, email=email)
                session.add(new_user)
                session.commit()
                break
            except sqlalchemy.exc.IntegrityError:
                session.rollback()
                print("Error! Please try another email address")
        initial_password = input("What is your password?")
        hashed_pass = generate_password_hash(initial_password)
        session.query(User).filter(User.email==email).update({'password' : hashed_pass})
        session.commit()
        print(f"User {new_user.first_name} {new_user.last_name} Created with account number: {new_user.id}")

            


    def csv_commit(file):
        pass

    def close_account():
            user_to_delete = input()

    def create_expense():
        pass

    def login():
        while True:
            email = input("Please enter email address ")
            password = input("Please enter password ")
            current_user = session.query(User).filter(User.email==email).first()
            if current_user != None and check_password_hash(current_user.password, password):
                print("Success!")
                return current_user
            else:
                print("Please try another email or password")