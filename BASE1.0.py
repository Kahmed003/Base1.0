import datetime
import matplotlib.pyplot as plt
import json
from collections import defaultdict


students = {}
ATTENDANCE_FILE = "attendance.txt"
STUDENT_DATA_FILE = "students_data.json"
DATE_TODAY = datetime.datetime.now().strftime('%Y-%m-%d')

def save_students_to_file():
    """Save the current students dictionary to a JSON file."""
    try:
        with open(STUDENT_DATA_FILE, 'w') as f:
            json.dump(students, f)
        print("Student data saved successfully.")
    except Exception as e:
        print("Error saving student data:", e)

def load_students_on_startup():
    """Automatically load students from the persistent JSON file at startup."""
    global students
    try:
        with open(STUDENT_DATA_FILE, 'r') as f:
            students = json.load(f)
        print("Student data loaded automatically!")
    except FileNotFoundError:
        print("No previous student data found. Please upload a student list.")

def load_students_from_file():
    """Allows a teacher to upload a student text file and populates the students dictionary."""
    global students
    file_path = input("Enter the path to the student file (e.g., 'students.txt'): ")
    try:
        with open(file_path, 'r') as file:
            students.clear()
            lines = file.readlines()
            print("\nLoading students...\n")
            for line in lines[1:]:
                if line.strip():
                    name, email, passkey = line.strip().split(',')
                    students[name.strip().lower()] = {
                        'email': email.strip().lower(),
                        'passkey': int(passkey.strip()),
                        'attendance': 0
                    }
            print("Student data loaded successfully!")
            save_students_to_file()  
    except FileNotFoundError:
        print("File not found. Please check the file path and try again.")
    except ValueError:
        print("File format error. Please ensure the file is formatted correctly (Name, Email, Passkey).")

def check_credentials():
    """Checks student credentials and marks attendance."""
    global DATE_TODAY
    name = input("Enter your name: ").lower()
    email = input("Enter your student email: ").lower()
    passkey = input("Enter valid student passkey: ")

    if name in students and students[name]['email'] == email and students[name]['passkey'] == int(passkey):
        print("WELCOME TO CLASS! HAVE A GREAT DAY, " + name.capitalize())
        students[name]['attendance'] += 1
        try:
            with open(ATTENDANCE_FILE, 'a') as file:
                file.write(name + " attended on " + DATE_TODAY + "\n")
        except Exception as e:
            print("Error writing to attendance file:", e)
        save_students_to_file() 
        return True
    else:
        print("INVALID DETAILS ENTRY. PLEASE TRY AGAIN!")
        return False

def display_attendance_records():
    """Displays attendance records and counts."""
    try:
        with open(ATTENDANCE_FILE, 'r') as file:
            records = file.readlines()
        print("\nAttendance Records:")
        for record in records:
            print(record.strip())
        print("\nAttendance Counts:")
        for name, data in students.items():
            print(f"{name.capitalize()}: {data['attendance']} days")
    except FileNotFoundError:
        print("No attendance records found.")

def plot_attendance_by_day():
    """Displays a bar chart for student attendance based on days of the week."""
    try:
        with open(ATTENDANCE_FILE, 'r') as file:
            records = file.readlines()

        
        day_counts = defaultdict(int)
        for record in records:
            if "attended on" in record:
                date_str = record.split(" attended on ")[1].strip()
                day_of_week = datetime.datetime.strptime(date_str, '%Y-%m-%d').strftime('%A')
                day_counts[day_of_week] += 1

        if not day_counts:
            print("No attendance data to display.")
            return

      
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        attendance_by_day = [day_counts.get(day, 0) for day in days_order]

        
        plt.figure(figsize=(10, 6))
        plt.bar(days_order, attendance_by_day)
        plt.xlabel("Days of the Week")
        plt.ylabel("Number of Students Attended")
        plt.title("Student Attendance by Day of the Week")
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("Attendance file not found. Please ensure attendance data exists.")

def teacher_menu():
    """Teacher menu to manage student records and attendance."""
    teacher_code = input("Enter teacher access code: ")
    if teacher_code == "KELLY":
        while True:
            action = input(
                "Enter 'upload' to upload a new student list, 'display' to show attendance records, "
                "'chart' to show attendance chart, or 'quit' to exit: "
            ).lower()
            if action == 'upload':
                load_students_from_file()
            elif action == 'display':
                display_attendance_records()
            elif action == 'chart':
                plot_attendance_by_day()
            elif action == 'quit':
                break
            else:
                print("Invalid action. Please enter 'upload', 'display', 'chart', or 'quit'.")
    else:
        print("Invalid teacher code.")


load_students_on_startup()


tries = 0
while True:
    user_type = input("Are you a student or teacher? (Enter 'student' or 'teacher'): ").lower()

    if user_type == 'student':
        if not students:
            print("No student records are loaded yet. Ask your teacher to upload a student list.")
            continue
        
        result = check_credentials()
        if result:
            break
        else:
            tries += 1
            if tries == 2:
                print("ACCOUNT TEMPORARILY LOCKED. CONTACT ADMINISTRATION FOR ASSISTANCE.")
                break
    
    elif user_type == 'teacher':
        teacher_menu()
    else:
        print("Invalid input. Please enter 'student' or 'teacher'.")
