from data_management import data_management
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user import User, Base
from database import init_db
import matplotlib






def main():
    init_db()
    main_loop = True
    while main_loop:
        current_user = None
        while True:
            login_menu = input('\n'.join(['\n',
            '1: Create user',
            '2: Login\n',
            
            'What would you like to do? (1-2): ']))

            match login_menu:
                case '1':
                    data_management.create_new_user()
                case'2':
                    current_user = data_management.login("cjolly@gmail.com","test")
                    break
                case _:
                    print('[italic red]Invalid response: Please enter a choice from the menut (1-2)[/italic red]')
        while True:
            main_menu = input('\n'.join(['\n',
            '1: Profile',
            '2: Dashbord',
            '3: Exit'
            
            'What would you like to do? (1-2): ']))

            match main_menu:
                case '1':
                    all_income=data_management.get_income("2010-1-10","2024-11-30",current_user)
                    for single_income in all_income:
                        print(single_income)
                case'2':
                    data_management.create_income(current_user, employer="Job", amount=1644)
                    data_management.create_income(current_user, employer="Job", amount=3443, Income_date="01-2-2021")
                case _:
                    pass
        
        
        # logout_menu = input('\n'.join(['\n',
        # '1: Create user',
        # '2: Login\n',
        
        # 'What would you like to do? (1-2): ']))

        # match logout_menu:
        #     case '1':
        #         data_management.create_new_user()
        #     case'2':
        #         current_user = data_management.login()
        #     case _,'':
        #         print('Invalid response: Please enter a choice from the menut (1-2)')

if __name__ == '__main__':
    main()