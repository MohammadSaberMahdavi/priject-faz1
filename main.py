from datetime import datetime
import sqlite3

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

