from data_management import data_management
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user import User, Base
from database import init_db


def main():
    init_db()

    # data_management.create_new_user()
    current_user = data_management.login()
    print(current_user)


if __name__ == '__main__':
    main()