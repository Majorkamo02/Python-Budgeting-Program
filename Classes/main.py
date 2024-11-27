from data_management import data_management
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user import User, Base
from database import init_db


def main():
    init_db()

    test_user2 = data_management.create_new_user()
    # test_user = data_management.create_new_user("Cameron","Jolly","cameron.l.jolly@gmail.com")
    # test_user3 = data_management.create_new_user("Parker","Thurston","parker.thurston@gmail.com")

    # session.add(test_user2)
    # session.commit()

if __name__ == '__main__':
    main()