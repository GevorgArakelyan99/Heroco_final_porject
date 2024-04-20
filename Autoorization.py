import base64
import os
import re
from sqlalchemy import String, Column, Integer, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///Users.db', echo=False)

connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'User_info'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


Base.metadata.create_all(engine)


class Check:
    __password = 0
    email = 0
    username = 0

    def __init__(self, username, email, password):
        self.email = email
        self.username = username
        self.__password = password

    def username_check(self, username):
        username = str(input("Please enter unique Username: "))
        while True:
            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user is None:
                break
            username = input(
                f"Sorry, the username '{username}' is already used. Please try another username :")
        return username

    def email_check(self, email):
        pattern = r"[^@]+@[^@]+\.[^@]+"
        email = str(input("Please enter unique Email address: "))
        while True:
            if re.match(pattern, email) and session.query(User).filter_by(email=email).first() is None:
                break
            email = input("Invalid email format or email already in use. Please try again.: ")
        return email

    def password_reg(self, password):
        password = str(input("Please enter Password: "))
        pattern = r"^(?=.*[A-Z])(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]).{8,}$"
        while not re.match(pattern, password):
            password = input(
                "Sorry password need to have.\nLength: At least 8 characters.\nUppercase Letter: At least one uppercase letter (A-Z).\nSpecial Character: At least one special character (e.g., @, #, $, etc.).\n")
        password = password.encode('ascii')
        encoded_pass = base64.b64encode(password)
        return encoded_pass


def user_add(username, email, password):
    user = User(username=username, email=email, password=password)
    session.add(user)
    session.commit()
def set_login_status(username):
    with open('login_status.txt', 'w') as file:
        file.write(f' {username} logged in')

def clear_login_status():
    if os.path.exists('login_status.txt'):
        os.remove('login_status.txt')

def is_logged_in():
    return os.path.exists('login_status.txt')


def login(log1, log2):
    check = False
    while not check:
        username = input("Please enter your Username: ")
        username_check = session.query(User).filter_by(username=username).first()
        if username_check:
            print(f"User found: Username - {username_check.username}")
        else:
            print("No user found with that username: ")
        password = input("Please enter your Password: ")
        password = password.encode('ascii')
        encoded_pass = base64.b64encode(password)
        password_check = session.query(User).filter_by(password=encoded_pass).first()
        if password_check:
            print("Login successful")
            set_login_status(username)
            check = True
        else:
            print("Login failed.")

