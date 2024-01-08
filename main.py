from datetime import datetime
import sqlite3

def main():
    while True:
        print("1.Register")
        print("2.Login")

        Select_Options = input(" Select_Options:")

        if Select_Options == "1":
            register_user()
        if Select_Options == "2":
            login_user()


class User:
    def __init__(self, user_id, username, email, password, user_type):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.user_type = user_type

    @classmethod
    def register(cls, username, email, password, user_type):
        # ایجاد اتصال به دیتابیس
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # ایجاد جدول اگر وجود نداشته باشد
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                email TEXT,
                password TEXT,
                user_type TEXT
            )
        ''')

        # ایجاد شناسه یکتا برای کاربر
        user_id = int(datetime.now().timestamp())

        # درج اطلاعات کاربر به دیتابیس
        cursor.execute('''
            INSERT INTO users (user_id, username, email, password, user_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, email, password, user_type))

        # ذخیره تغییرات و بستن اتصال
        conn.commit()
        conn.close()

        # ایجاد نمونه جدید از کاربر
        new_user = cls(user_id, username, email, password, user_type)
        return new_user

    @classmethod
    def login(cls, username, password):
        # اتصال به دیتابیس
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # جستجو بر اساس نام کاربری و رمز عبور
        cursor.execute('''
                SELECT * FROM users
                WHERE username = ? AND password = ?
            ''', (username, password))

        user_data = cursor.fetchone()

        # بستن اتصال
        conn.close()

        if user_data:
            # ایجاد نمونه کاربر در صورت موفقیت
            user = cls(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
            return user
        else:
            return None


def register_user():
    print("Welcome to the Registration Process!")

    # گرفتن ورودی‌های مورد نیاز برای ثبت نام
    username = input("Enter your username: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    user_type = input("Enter your user type (e.g., patient, staff): ")

    # صدا زدن متد register و دریافت نتیجه
    registered_user = User.register(username, email, password, user_type)

    # چاپ اطلاعات کاربر ثبت شده
    print("\nRegistration Successful!")
    print("User ID:", registered_user.user_id)
    print("Username:", registered_user.username)
    print("Email:", registered_user.email)
    print("User Type:", registered_user.user_type)

def login_user():
    print("Welcome to the Login Process!")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    logged_in_user = User.login(username, password)
    if logged_in_user:
        print("\nLogin Successful!")
        print("Username:", logged_in_user.username)
        print("Email:", logged_in_user.email)
        print("User Type:", logged_in_user.user_type)

        print("1.Update Profile")
        print("2")
        print("3.Back")
        Login_Options = input("Login_Options:")
        if Login_Options == "1":
            pass

        # if l_o=="2":

        if Login_Options == "3":
            main()
    else:
        print("\nLogin Failed! Invalid username or password.")
        main()

