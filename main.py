from datetime import datetime
import sqlite3
import re
import requests

def is_valid_email(email):
    # چک کردن فرمت درست ایمیل
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)
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

    @classmethod
    def update_profile(cls, user_id, new_username, new_email, new_password):
        # اتصال به دیتابیس
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # جستجو بر اساس شناسه کاربر
        cursor.execute('''
            SELECT * FROM users
            WHERE user_id = ?
        ''', (user_id,))

        user_data = cursor.fetchone()

        if user_data:
            # اگر کاربر با شناسه مورد نظر یافت شد
            # اپدیت اطلاعات
            cursor.execute('''
                UPDATE users
                SET username = ?, email = ?, password = ?
                WHERE user_id = ?
            ''', (new_username, new_email, new_password, user_id))

            # ذخیره تغییرات و بستن اتصال
            conn.commit()
            conn.close()

            # ایجاد نمونه کاربر با اطلاعات به‌روزرسانی شده
            updated_user = cls(user_id, new_username, new_email, new_password, user_data[4])
            return updated_user
        else:
            # اگر کاربر با شناسه مورد نظر یافت نشد
            conn.close()
            return None

    def view_appointments(self):
            # نمایش نوبت‌های اختصاص یافته به کاربر
            dbase = sqlite3.connect('users.db')
            cursor = dbase.cursor()

            view_query = f'''
                SELECT * FROM appointments
                WHERE user_id = ?
            '''

            cursor.execute(view_query, (self.user_id,))
            appointments = cursor.fetchall()

            dbase.close()

            if appointments:
                print("Appointments:")
                for appointment in appointments:
                    print(appointment)
            else:
                print("You dont have any Appointments")


def register_user():
    print("Welcome to the Registration Process!")

    # گرفتن ورودی‌های مورد نیاز برای ثبت نام
    username = input("Enter your username: ")
    email = input("Enter your email: ")
    while not is_valid_email(email):
        print("Invalid email format. Please enter a valid email.")
        email = input("Enter your email: ")
    password = input("Enter your password: ")
    user_type = input("Enter your user type (Monshi,Bimar): ")
    while user_type not in ['Bimar', 'Monshi']:
        print("Invalid user type. Please enter either 'Bimar' or 'Monshi'.")
        user_type = input("Enter your user type (Bimar/Monshi): ").lower()

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
        print("User ID:", logged_in_user.user_id)
        print("Username:", logged_in_user.username)
        print("Email:", logged_in_user.email)
        print("User Type:", logged_in_user.user_type)
        if logged_in_user:
            if logged_in_user.user_type == "Monshi":
                monshi_menu(logged_in_user)
            elif logged_in_user.user_type == "Bimar":
                # اگر نوع کاربر بیمار باشد، منو مخصوص بیمار فراخوانی شود (تابع مربوطه تعریف شود)
                bimar_menu(logged_in_user)
            else:
                print("Invalid user type.")




def update_user_profile():
    print("Welcome to the Profile Update Process!")

    # گرفتن ورودی‌های مورد نیاز برای آپدیت پروفایل
    user_id = int(input("Enter your user ID: "))
    new_username = input("Enter your new username (leave empty to keep current): ")
    new_email = input("Enter your new email (leave empty to keep current): ")
    while not is_valid_email(new_email):
        print("Invalid email format. Please enter a valid email.")
        new_email = input("Enter your email: ")
    new_password = input("Enter your new password (leave empty to keep current): ")

    # صدا زدن متد update_profile و دریافت نتیجه
    updated_user = User.update_profile(user_id, new_username, new_email, new_password)

    if updated_user:
        print("\nProfile Update Successful!")
        print("Updated User ID:", updated_user.user_id)
        print("Updated Username:", updated_user.username)
        print("Updated Email:", updated_user.email)
        print("Updated User Type:", updated_user.user_type)
    else:
        print("\nUser with the provided ID not found. Profile update failed.")


class view_all():
    @classmethod
    def view_all_users(cls):
        # نمایش همه کاربران در یک جدول
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # اجرای کوئری برای دریافت همه کاربران
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()

        # بستن اتصال
        conn.close()

        if users:
            print("All Users:")
            print("{:<20} {:<20} {:<20} {:<20} ".format("User ID", "Username", "Email", "User Type"))
            print("-" * 90)
            for user in users:
                print("{:<20} {:<20} {:<20} {:<20} ".format(user[0], user[1], user[2], user[4]))
        else:
            print("No users found.")


class Clinic:
    def __init__(self, clinic_id, name, address, contact_info, services, availability):
        self.clinic_id = clinic_id
        self.name = name
        self.address = address
        self.contact_info = contact_info
        self.services = services
        self.availability = availability
        self.appointments = []

    def add_clinic(self, clinic_id, name, address, contact_info, services, availability):
        # connect to database
        conn = sqlite3.connect('clinics.db')
        curser = conn.cursor()
        # Create the table if it does not exist
        curser.execute('''
            CREATE TABLE IF NOT EXISTS clinics (
                clinic_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                address TEXT,
                contact_info TEXT,
                services TEXT,
                availability TEXT
            )
        ''')

        # create query
        curser.execute('''
            INSERT INTO clinics (name, address, contact_info, services, availability)''')

        # commit changes
        conn.commit()
        # close connection
        conn.close()

        # create new clinic object
        new_clinic = Clinic(clinic_id, name, address, contact_info, services, availability)

        return new_clinic

    def update_clinic_info(self, new_name, new_address, new_contact_info, new_services):
        # connect to database
        conn = sqlite3.connect('clinics.db')
        curser = conn.cursor()

        # search for clinic with the name of clinic
        curser.execute('''
            select * from clinics 
            where name =?''',
                       (new_name,))
        # check if clinic exists
        if curser.fetchone():
            # update the clinic info
            curser.execute('''
                UPDATE clinics
                SET name =?, address =?, contact_info =?, services =?
                WHERE name =?''',
                           (new_name, new_address, new_contact_info, new_services, new_name))

            # commit changes
            conn.commit()
            # close connection
            conn.close()
            # create new clinic object
            update_clinic = Clinic(self.clinic_id, new_name, new_address, new_contact_info, new_services,
                                   self.availability)
            print(f"Clinic {new_name} with ID {self.clinic_id} updated successfully.")
            return update_clinic

    def view_appointment(self, appointment_id):
        # connect to database
        conn = sqlite3.connect('appointments.db')
        cursor = conn.cursor()

        # search for appointment using appointment_id
        cursor.execute('''
            SELECT * FROM appointments
            WHERE appointment_id = ?''',
                       (appointment_id,))

        appointment_data = cursor.fetchone()

        if appointment_data:
            appointment_id, date, time, patient_name = appointment_data
            print(f"Appointment ID: {appointment_id} Date: {date} Time: {time} Patient Name: {patient_name}")
            return appointment_data
        else:
            print("Appointment not found.")
            
    def set_availability(self, clinic_id, reserved):
        # Make a POST request to the API to reserve slots
        url = "http://127.0.0.1:5000/reserve"
        data = {
            "id": clinic_id,
            "reserved": reserved
        }
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            print(f"Slots reserved successfully for clinic with ID {clinic_id}")
        else:
            print(f"Failed to reserve slots for clinic with ID {clinic_id}")


def register_clinic():
    print("Welcome to the Registration Process!")

    # getting input from user
    clinic_id = input("Enter your clinic ID: ")
    name = input("Enter your clinic name: ")
    address = input("Enter your clinic address: ")
    contact_info = input("Enter your clinic contact info: ")
    services = input("Enter your clinic services: ")
    availability = input("Enter your clinic availability: ")

    # creating new clinic object
    new_clinic = Clinic.add_clinic(clinic_id, name, address, contact_info, services, availability)

    # printing results
    print(f"Clinic {new_clinic.name} with ID {new_clinic.clinic_id} added successfully.")


def update_clinic_info():
    print("Welcome to the Clinic Info Update Process!")

    # getting input from user
    new_name = input("Enter the new clinic name: ")
    new_address = input("Enter the new clinic address: ")
    new_contact_info = input("Enter the new clinic contact info: ")
    new_services = input("Enter the new clinic services: ")

    # creating new clinic object
    update_clinic = Clinic.update_clinic_info(new_name, new_address, new_contact_info, new_services)

    # printing results
    if update_clinic:
        print(f"Clinic {update_clinic.name} with ID {update_clinic.clinic_id} updated successfully.")





def main():
    while True:
        print("Welcome to the Clinic Reservation System!")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            register_user()
        elif choice == "2":
            logged_in_user = login_user()

        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

def monshi_menu(logged_in_user):
    while True:
        print("\nMonshi Menu:")
        print("1. View Appointments")
        print("2. Add Appointment")
        print("3. Increase Appointment Capacity")
        print("4. View User informations")
        print("5. Update Profile")
        print("6. Logout")

        monshi_choice = input("Enter your choice (1-6): ")

        if monshi_choice == "1":
            # اجرای تابع مربوط به نمایش وقت‌های رزرو شده
            view_appointments(logged_in_user)
        elif monshi_choice == "2":
            # اجرای تابع مربوط به افزودن وقت جدید
            add_appointment(logged_in_user)
        elif monshi_choice == "3":
            # اجرای تابع مربوط به افزایش ظرفیت نوبت دهی
            increase_appointment_capacity(logged_in_user)

        elif monshi_choice == '4':
            view_all.view_all_users()

        elif monshi_choice=="5":
            update_user_profile()


        elif monshi_choice == "6":
            print("Logout Successful!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

def bimar_menu(logged_in_user):
    while True:
        print("\nBimar Menu:")
        print("1. View Appointments")
        print("2. Cancel Appointment")
        print("3. Update Profile")
        print("4. Logout")

        bimar_choice = input("Enter your choice (1-4): ")

        if bimar_choice == "1":
            # اجرای تابع مربوط به نمایش وقت‌های رزرو شده برای بیمار
            view_appointments_for_bimar(logged_in_user)
        elif bimar_choice == "2":
            # اجرای تابع مربوط به لغو وقت نوبت
            cancel_appointment(logged_in_user)
        elif bimar_choice=="3":
            update_user_profile()
        elif bimar_choice == "4":
            print("Logout Successful!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


main()
