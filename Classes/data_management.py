import sqlalchemy
from user import User
from database import session
from transaction import UserTransaction
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from income import Income
from expense import Expense
from savings import Save


def get_valid(question, warning, type):
    while(True):
        try:
            if type == "int":
                answer = int(input(question))
            elif type == "float":
                answer = float(input(question))
            else:
                print("Error.  Invalid type sent to get_valid.")
                return None
            return answer
        except:
            print(warning + "\n")


class data_management(User):
    def create_new_user(first,last,email, password):        
        # first = input("What is your first name? ")
        # last = input("What is your last name? ")
        # loop1=True   
        
        try:
            UserTransaction()
            Income()
            Expense()
            Save()
            new_user = User(first_name=first, last_name=last, email=email)
            session.add(new_user)
            session.commit()
            hashed_pass = generate_password_hash(password)
            session.query(User).filter(User.email==email).update({'password' : hashed_pass})
            session.commit()
            print(f"User {new_user.first_name} {new_user.last_name} Created with account number: {new_user.id} \n\n Please login using your new login credentials")
            return new_user
        except sqlalchemy.exc.IntegrityError:
            session.rollback()
            print("Error! Please try another email address")
            return None

    def csv_commit(file):
        pass

    def login(email,password):
        
        # email = input("Please enter email address ")
        # password = input("Please enter password ")
        current_user = session.query(User).filter(User.email==email).first()
        if current_user != None and check_password_hash(current_user.password, password):
            print("You are now logged in!")
            return current_user
        else:
            print("Please try another email or password")
            return None

    def close_account(current_user):
        session.delete(current_user)
        session.commit()
        return "sucess"

    def create_expense(current_user: User, amount, category, storename, expense_date=None):
        new_expense = Expense(storename=storename,amount=amount,category=category,date=datetime.datetime.strptime(expense_date, '%Y-%m-%d').date() if expense_date else datetime.date.today())
        session.add(new_expense)
        current_user.Transactions.append(new_expense)
        session.commit()

    def get_expense(start_date, end_date, current_user:User):
        expense = session.query(Expense).filter(Expense.user_id == current_user.id, Expense.date.between(f"{start_date}",f"{end_date}")).all()
        return expense

    def create_income(current_user:User, amount, employer, Income_date=None):
        new_income = Income(amount=amount,employer=employer,date=datetime.datetime.strptime(Income_date, '%Y-%m-%d').date() if Income_date else datetime.date.today())
        session.add(new_income)
        current_user.Transactions.append(new_income)
        session.commit()

    def get_income(start_date, end_date,current_user:User):
        income = session.query(Income).filter(Income.user_id == current_user.id, Income.date.between(f"{start_date}",f"{end_date}")).all()
        return income

    def create_saving(current_user: User, amount, account_name, account_type,saving_date=None):
        new_saving = Save(date=datetime.datetime.strptime(saving_date, '%Y-%m-%d').date() if saving_date else datetime.date.today(), amount=amount,account_name=account_name, account_type=account_type )
        session.add(new_saving)
        current_user.Transactions.append(new_saving)
        session.commit()

    def get_saving(start_date, end_date, current_user:User):
        save = session.query(Save).filter(Save.user_id == current_user.id, Save.date.between(f"{start_date}",f"{end_date}")).all()
        return save