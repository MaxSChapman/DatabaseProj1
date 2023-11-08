import csv
import random
import sqlite3
from sqlite3 import Error

# Configuration for database connection
DATABASE = 'students.db'
states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California",
    "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
    "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
    "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]
faculty_advisors = [
    'Rene', 'Cap\'n Thomas', 'Jake from State Farm', 'Kobe'
]


# Function to connect to the SQLite database
def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


# Function to create table
def create_table(conn):
    """Create a table from the students.sql file"""
    try:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Students (
                          StudentId INTEGER PRIMARY KEY,
                          FirstName TEXT,
                          LastName TEXT,
                          GPA REAL,
                          Major TEXT,
                          FacultyAdvisor TEXT,
                          Address TEXT,
                          City TEXT,
                          State TEXT,
                          ZipCode TEXT,
                          MobilePhoneNumber TEXT,
                          isDeleted INTEGER DEFAULT 0
                        );""")
    except Error as e:
        print(e)


# Function to import CSV into the database
def import_students_from_csv(conn, csv_file_path):
    """Import data from a CSV file into the Students table"""
    cursor = conn.cursor()
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute('''
                        INSERT INTO Students (FirstName,LastName,GPA,Major,FacultyAdvisor,Address,City,
                                              State,ZipCode,MobilePhoneNumber)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                row["FirstName"], row["LastName"], row["GPA"], row["Major"], random.choice(faculty_advisors),
                row["Address"], row["City"], row["State"], row["ZipCode"], row["MobilePhoneNumber"]))
    conn.commit()


# Function to display all students
def display_all_students(conn):
    """Display all students and all of their attributes"""
    cursor = conn.cursor()
    cursor.execute('''SELECT *
                      From Students;''')
    for row in cursor:
        print(row)
    conn.commit()


# Function to add a new student
def validateString(input):
    if all(c.isalpha() or c.isspace() for c in input):
        return input
    return None
def validateReal(input):
    try:
        fInput = float(input)
        if 0.00 <= fInput <= 5.00:
            return fInput
    except ValueError:
        return None
def validateAddress(input):
    if all(c.isalnum() or c.isspace() for c in input):
        return input
    return None
def validateState(input):
    if input in states:
        return input
    return None
def validateInteger(input):
    try:
        return int(input)
    except ValueError:
        return None
def validateZip(input):
    if len(input) != 5:
        return None
    return validateInteger(input)
def validateID(input, conn):
    iInput = validateInteger(input)
    if iInput is None:
        print("Non-integer input. ")
        return None
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNT(*) FROM Students WHERE StudentId = ?''', (iInput,))
    if cursor.fetchone()[0] == 1:
        return iInput
    print("That student id does not currently exist in the database.")
    return None


def add_new_student(conn):
    """Add a new student with all attributes"""
    firstName = None
    while firstName is None:
        print("Please enter student's first name. No numbers or special characters will be accepted.")
        firstName = validateString(input())

    lastName = None
    while lastName is None:
        print("Please enter student's last name. No numbers or special characters will be accepted.")
        lastName = validateString(input())

    GPA = None
    while GPA is None:
        print("Please enter student's GPA. Only real numbers between 0.00 and 5.00 will be accepted")
        GPA = validateReal(input())

    major = None
    while major is None:
        print("Please enter student's major. No numbers or special characters will be accepted.")
        major = validateString(input())

    faculty_advisor = None
    while faculty_advisor is None:
        print("Please enter student's faculty advisor. No numbers or special characters will be accepted.")
        faculty_advisor = validateString(input())

    address = None
    while address is None:
        print("Please enter student's address. No special characters will be accepted.")
        address = validateAddress(input())

    city = None
    while city is None:
        print("Please enter student's city of residence. No numbers or special characters will be accepted.")
        city = validateString(input())

    state = None
    while state is None:
        print("Please enter student's state of residence, in full.. "
              "Make sure the first letter is capitalized."
              "Only valid states will be accepted.")
        state = validateState(input())

    zipCode = None
    while zipCode is None:
        print("Please enter student's zipCode. Only 5 integer sequences will be accepted.")
        zipCode = validateZip(input())

    phoneNo = None
    while phoneNo is None:
        print("Please enter student's mobile number. Enter only as a numerical sequence - "
              "no dashes or other special characters will be accepted.")
        phoneNo = validateInteger(input())

    cursor = conn.cursor()
    cursor.execute('''
                      INSERT INTO Students (FirstName,LastName,GPA,Major,FacultyAdvisor,Address,City,
                                            State,ZipCode,MobilePhoneNumber)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                      ''', (
                      firstName, lastName, GPA, major, faculty_advisor, address, city, state, zipCode, phoneNo)
                   )
    conn.commit()
    print("Insertion successful")

# Function to update a student
def update_student(conn):
    """Update a student's major, advisor, and mobile phone number using their StudentId"""
    sID = None
    while sID is None:
        print("Please enter the student ID of the student you would like to update")
        sID = validateID(input(), conn)

    print("Only some features are editable. Would you like to update: \n1. Major\n2. Advisor"
          "\n3. Mobile Phone Number\nPlease type the number of the attribute you wish to change.")

    userInput = input()
    while userInput not in ["1", "2", "3"]:
        print("Invalid input. Please type only 1, 2, or 3")
        userInput = input()

    cursor = conn.cursor()

    if userInput == "1":
        attributeToChange = "Major"
        newAttribute = None
        while newAttribute is None:
            print("Please enter student's new major. No numbers or special characters will be accepted.")
            newAttribute = validateString(input())

    elif userInput == "2":
        attributeToChange = "FacultyAdvisor"
        newAttribute = None
        while newAttribute is None:
            print("Please enter student's new faculty advisor. No numbers or special characters will be accepted.")
            newAttribute = validateString(input())

    elif userInput == "3":
        attributeToChange = "MobilePhoneNumber"
        newAttribute = None
        while newAttribute is None:
            print("Please enter student's new mobile number. Enter only as a numerical sequence - "
                  "no dashes or other special characters will be accepted.")
            newAttribute = validateInteger(input())

    else:
        print("An error occurred during update")
        return None

    sqlCommand = f'''
                      UPDATE Students
                      SET {attributeToChange} = ?
                      WHERE StudentID = ?;'''
    cursor.execute(sqlCommand, (newAttribute, sID))
    conn.commit()

    print("Update has been successfully completed.")


# Function to soft-delete a student by StudentId
def soft_delete_student(conn):
    """Perform a soft delete on a student by setting isDeleted to true"""
    sID = None
    while sID is None:
        print("Please enter the student ID of the student you would like to delete")
        sID = validateID(input(), conn)

    cursor = conn.cursor()
    cursor.execute('''
                      UPDATE Students
                      SET isDeleted = ?
                      WHERE StudentID == ?;
                   ''', (1, sID))
    conn.commit()

    print("Deletion successful.")


# Function to search/display students by Major, GPA, City, State, and Advisor
def search_students(conn):
    """Search and display students by Major, GPA, City, State, and Advisor"""
    print("Will you be searching the student database by:"
          "\n1. Major\n2. GPA\n3. City\n4. State\n5. Advisor"
          "\nEnter the integer corresponding to your goal.\n")
    userInput = input()
    while userInput not in ["1", "2", "3", "4", "5"]:
        print("Invalid input. Please choose an integer 1-5 corresponding to your desired functionality.")
        userInput = input()

    if userInput == "1":
        attributeToChange = "Major"
        newAttribute = None
        while newAttribute is None:
            print("Please enter student's major. No numbers or special characters will be accepted.")
            newAttribute = validateString(input())

    elif userInput == "2":
        attributeToChange = "GPA"
        newAttribute = None
        while newAttribute is None:
            print("Please enter student's GPA. Only real numbers between 0.00 and 5.00 will be accepted")
            newAttribute = validateReal(input())

    elif userInput == "3":
        attributeToChange = "City"
        newAttribute = None
        while newAttribute is None:
            print("Please enter student's city of residence. No numbers or special characters will be accepted.")
            newAttribute = validateString(input())

    elif userInput == "4":
        attributeToChange = "state"
        newAttribute = None
        while newAttribute is None:
            print("Please enter student's state of residence, in the form of it's abbreviation. "
                  "Make sure both letters are capitalized."
                  "Only valid abbreviations will be accepted.")
            newAttribute = validateState(input())

    elif userInput == "5":
        attributeToChange = "FacultyAdvisor"
        newAttribute = None
        while newAttribute is None:
            print("Please enter student's faculty advisor. No numbers or special characters will be accepted.")
            newAttribute = validateString(input())

    cursor = conn.cursor()
    sqlCommand = f'''
                      SELECT * FROM Students
                      WHERE {attributeToChange} = ?
                      '''
    cursor.execute(sqlCommand, (newAttribute,))
    for row in cursor:
        print(row)


# Main function to orchestrate the operations
def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE)

    if conn is not None:
        cursor = conn.cursor()
        # Create table if it doesn't exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (DATABASE,))
        table_exists = cursor.fetchone()

        # If the table does not exist, create it
        if not table_exists:
            create_table(conn)

        print("Database connection has been established.\n")
        userInput = None
        while userInput != "7":
            print("\n\n\nWhat would you like to do?\n1. Import students csv file\n2. Display all students"
                  "\n3. Add new student\n4. Update a student record\n5. Soft delete student record"
                  "\n6. Search students by common attribute\n7. Exit program\nEnter an integer 1-7")
            userInput = input()
            while userInput not in ["1", "2", "3", "4", "5", "6", "7"]:
                print(
                    "Invalid input. Only integers between 1-7 will be accepted, referencing the 7 different options.")
                userInput = input()

            if userInput == "1":
                import_students_from_csv(conn, 'students.csv')
            elif userInput == "2":
                display_all_students(conn)
            elif userInput == "3":
                add_new_student(conn)
            elif userInput == "4":
                update_student(conn)
            elif userInput == "5":
                soft_delete_student(conn)
            elif userInput == "6":
                search_students(conn)

            # Wait for user to return before prompting main menu again
            print("Enter any input to continue back to main menu")
            input()
        # Commit any changes and close the database connection
        conn.commit()
        conn.close()
    else:
        print("Error! Cannot create the database connection.")


if __name__ == '__main__':
    main()
