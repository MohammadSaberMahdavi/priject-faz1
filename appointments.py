
class AppointmentScheduler:
    def __init__(self):
        self.conn = sqlite3.connect('appointments.db')
        self.cursor = self.conn.cursor()


    def get_patient_appointments(self, user_id):
        query = '''
            SELECT date, time
            FROM appointments
            WHERE user_id = ? AND reserved = 1
        '''
        self.cursor.execute(query, (user_id,))
        patient_appointments = self.cursor.fetchall()
        return patient_appointments

    def view_patient_appointments(self, user_id):
        patient_appointments = self.get_patient_appointments(user_id)
        if patient_appointments:
            print("Your Appointments:")
            for idx, (date, time) in enumerate(patient_appointments, start=1):
                print(f"{idx}. Date: {date}, Time: {time}")
            return patient_appointments
        else:
            print("You have no scheduled appointments.")
            return None

    def cancel_appointment(self, user_id):
        patient_appointments = self.view_patient_appointments(user_id)

        if patient_appointments:
            choice = int(input("Enter the number corresponding to the appointment you want to cancel: "))
            if 1 <= choice <= len(patient_appointments):
                canceled_appointment = patient_appointments[choice - 1]
                date, time = canceled_appointment

                # Update the 'reserved' status to 0 (available) for the canceled appointment
                query = '''
                    UPDATE appointments
                    SET reserved = 0
                    WHERE patient_id = ? AND date = ? AND time = ?
                '''
                self.cursor.execute(query, (user_id, date, time))
                self.conn.commit()
                print(f"Appointment on {date} at {time} canceled successfully!")
            else:
                print("Invalid choice. Please enter a valid number.")
