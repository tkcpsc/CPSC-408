import sqlite3
import csv
import random


# Connect to Database (StudentDB.db)
conn = sqlite3.connect('/Users/tommykudey/Library/Mobile Documents/com~apple~CloudDocs/Academic/Fall 2023/CPSC 408/StudentDB.db') # establish connection
mycursor = conn.cursor()


# 2.a)
# Populating fields from student.csv

# List of 10 random names (replace with your actual list of names)
facultyAdvisor = ["John Foo", "Jane Bar", "Michael Phelps", "Emily William", "David ball", "Sarah far", "Robert long", "Emma boo", "William turner", "Olivia rod"]

def populateWithCSV(pathToFile):
    with open(pathToFile, mode='r') as file:
        csvFile = csv.reader(file)
        for row in csvFile:
            random_name = random.choice(facultyAdvisor)
            mycursor.execute(
                "INSERT INTO Student(FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (row[0], row[1], row[8], row[7], random_name, row[2], row[3], row[4], row[5], row[6], 0)
            )

        conn.commit()

# Print Student from StudentId - Helper function
def printStudent(StudentId):
    mycursor.execute("SELECT * FROM Student WHERE StudentId = ?;", (StudentId,))
    print(mycursor.fetchall())

def printLastStudent():
    mycursor.execute("SELECT * FROM Student ORDER BY StudentId DESC LIMIT 1")
    print(mycursor.fetchall())

# 2.b)
def printAll():
    mycursor.execute("Select * from Student;")
    rows2 = mycursor.fetchall()
    for row2 in rows2:
        print(row2)

# 2.c)
# Values for the new row
# newStudent = (4, 'D', ... , n)
def addStudent(newStudent):
    # SQL statement to insert a new row
    insertQuery = "INSERT INTO Student (FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
    mycursor.execute(insertQuery, newStudent)
    conn.commit()

    # Verification
    print("Added New Student:")
    printLastStudent()

# 2.d)
def updateStudent(StudentId, Major, FacultyAdvisor, MobilePhoneNumber):
    mycursor.execute("UPDATE Student SET Major = ?, Advisor = ?, MobilePhoneNumber = ? WHERE StudentId = ?", (Major, FacultyAdvisor, MobilePhoneNumber,StudentId,))
    conn.commit()

    # Verification
    print("Updated Student: ")
    printStudent(StudentId)

# 2.e)
def deleteStudent(StudentId):
    mycursor.execute("UPDATE Student SET isDeleted = 1 WHERE StudentId = ?", (StudentId,))
    conn.commit()

    # Verification
    print("Deleted Student: ")
    printStudent(StudentId)

# 2.f)
# 2.f.OrderBy) Order Data.
def orderBy(column):
    # Check if the provided column name is valid (security measure)
    valid_columns = ["Major", "GPA", "City", "State", "Advisor"]  # Add more valid column names as needed
    if column not in valid_columns:
        print("Invalid column name.")
        return
    orderQuery = f"SELECT * FROM Student ORDER BY {column};"
    mycursor.execute(orderQuery)
    rows2 = mycursor.fetchall()
    for row2 in rows2:
        print(row2)

    conn.commit()

# 2.f.Query) Search For Data.
def searchFor(conditions): # sample input would be a string: queryCriteria = "Major = Computer Science AND GPA > 3"

    searchQuery = "SELECT * FROM Student WHERE " + conditions
    mycursor.execute(searchQuery + ";")
    rows2 = mycursor.fetchall()
    for row2 in rows2:
        print(row2)

    conn.commit()


# 1)
# If the table does not exist, then this creates it.
#     mycursor.execute("Delete table Student")
#     conn.commit()

pathToFile = '/Users/tommykudey/Library/Mobile Documents/com~apple~CloudDocs/Academic/Fall 2023/CPSC 408/students.csv'


try:
    mycursor.execute("Select * from Student;")
except:
    print("Creating New Table Student.")
    mycursor.execute("CREATE TABLE Student(StudentId INTEGER PRIMARY KEY, FirstName TEXT, LastName TEXT, GPA REAL, Major TEXT, FacultyAdvisor TEXT, Address TEXT, City TEXT, State TEXT, ZipCode TEXT, MobilePhoneNumber TEXT, isDeleted INTEGER);")
    populateWithCSV(pathToFile)

table_schema = {
    'StudentId': int,
    'FirstName': str,
    'LastName': str,
    'GPA': float,
    'Major': str,
    'FacultyAdvisor': str,
    'Address': str,
    'City': str,
    'State': str,
    'ZipCode': str,
    'MobilePhoneNumber': str,
    'isDeleted': int
}
def is_valid_column_name(input_value, table_schema):
    return input_value in table_schema


def getValidInput(columnName):
    while True:
        try:
            userInput = input(f"Enter {columnName}: ")
            # Attempt to convert the input to the appropriate data type
            return table_schema[columnName](userInput)
        except (ValueError, KeyError):
            print(f"Invalid input for {columnName}. Please provide a valid {table_schema[columnName].__name__}.")


print("\nPath to Database: ", pathToFile)

while True:
    print("\nSelect one of the following options:")
    print("  1. Change Database file path")
    print("  2. Display All Students and their attributes")
    print("  3. Add New Students (all attributes required)")
    print("  4. Update Students (Major, Advisor, MobilePhoneNumber)")
    print("  5. Delete Students by StudentId (soft delete, set isDeleted to 1)")
    print("  6. Display Students by Major, GPA, City, State, and Advisor")
    print("  7. Search Students by Major, GPA, City, State, and Advisor")
    print("  8. Exit the program\n")
    userInput = input(f"Enter Number 1-8: ")
    if userInput == "1":
        pathToFile = userInput
        mycursor.execute("Drop table student")
        conn.commit()
        print("Creating New Table Student from: ", pathToFile)
        mycursor.execute(
        "CREATE TABLE Student(StudentId INTEGER PRIMARY KEY, FirstName TEXT, LastName TEXT, GPA REAL, Major TEXT, FacultyAdvisor TEXT, Address TEXT, City TEXT, State TEXT, ZipCode TEXT, MobilePhoneNumber TEXT, isDeleted INTEGER);")
        populateWithCSV(pathToFile)
        conn.commit()

    elif userInput == "2":
        printAll()
    elif userInput == "3":

        addStudent([getValidInput("FirstName"),
                   getValidInput("LastName"),
                   getValidInput("GPA"),
                   getValidInput("Major"),
                   getValidInput("FacultyAdvisor"),
                   getValidInput("Address"),
                   getValidInput("City"),
                   getValidInput("State"),
                   getValidInput("ZipCode"),
                   getValidInput("MobilePhoneNumber"),
                   getValidInput("isDeleted")
        ])
    elif userInput == "4":
        updateStudent(getValidInput("Major"), getValidInput("FacultyAdvisor"), getValidInput("MobilePhoneNumber"), getValidInput("StudentId"))
        printAll()
    elif userInput == "5":
        deleteStudent(getValidInput("StudentId"))
    elif userInput == "6":
        # try:
        input_column = input("Enter a column name to Order by: ")
        while True:
            if is_valid_column_name(input_column, table_schema):
                orderBy(input_column)
                break
        # except:
        #     print("Error, Invalid Input")
    elif userInput == "7":
        try:
            searchFor(input("sample input would be a string: (Major = Computer Science AND GPA > 3)"))
        except:
            print("Error, Invalid Input")
    elif userInput == "8":
        break
    else:
        print("SELECT AN OPERATION 1-8 (ENTER A VALID INTEGER 1-8): ")





mycursor.close()













