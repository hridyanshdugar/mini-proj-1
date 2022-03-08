from getpass import getpass
from login import Login
database_path = "./mini-proj.db"


def welcome():
    print('*'*100)
    print("* {:^96s} *".format("Movie System"))
    print("*"*100)


def login():
    userid = input("Enter ID: ")
    pwd = getpass("Enter password: ")

    # Try logging in
    log = Login(userid, pwd, database_path)
    success = log.login()
    while not success:
        print("Please select an option: ")
        print("1. Try again")
        print("2. Register as a new user")
        choice = input("Choice :")
        if choice == '1':
            userid = input("Enter ID: ")
            pwd = getpass("Enter password: ")
            log = Login(userid, pwd, database_path)
            success = log.login()
        elif choice == '2':
            userid = input("Enter ID: ")
            name = input("Enter your name: ")
            pwd = getpass("Enter password: ")
            log = Login(userid,pwd, database_path)
            success = log.signup(name)
            if success:
                success = log.login()
    return log


def login_screen():

    # Print the welcome sign
    welcome()

    # Try to login or register the user if the user can't login
    log = login()


    print("Welcome, "+ log.name)



login_screen()