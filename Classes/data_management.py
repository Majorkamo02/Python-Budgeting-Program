import sqlalchemy
from .user import User, session

class data_management(User):
    def create_new_user(first, last, email):        
        try:
            new_user = User(first_name=first, last_name=last, email=email)
            session.add(new_user)
            session.commit()
            print(f"User {new_user.first_name} {new_user.last_name} Created with account number: {new_user.account_number}")
            return new_user
        except sqlalchemy.exc.IntegrityError:
            print("Error! Please try another email address")


    def csv_commit(file):
        pass

    def close_account():
        pass

    def create_expense():
        pass

#test
    