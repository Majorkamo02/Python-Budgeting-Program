from Classes.user import User
from Classes.data_management import data_management

def main():

    test_user2 = data_management.create_new_user("Slader","Radmall","radmallslader@gmail.com")
    test_user = data_management.create_new_user("Cameron","Jolly","cameron.l.jolly@gmail.com")
    test_user3 = data_management.create_new_user("Parker","Thurston","parker.thurston@gmail.com")



if __name__ == '__main__':
    main()