#!/usr/bin/python3

import sqlite3
import subprocess
import sys
import os
import re


def interactiveMenu(menuitems: dict, prompt: str = "Select",
        exclude: bool = False, multiple: bool = True):
    items = list(menuitems.keys())
    
    print(f"\n{prompt}:\n")
    for i, item in enumerate(items):
        print(f"\t{i + 1}: {item}")
    print("\n\t0: Cancel\n")

    strMultiple = f"""Select one{' or multiple (eg: "1", "1 4 2")' if multiple else ''}"""

    indices = input(f"""{strMultiple}\n : """).split(" ")
    
    valid = 0x0
    for i in indices:
        try:
            v = int(i)
            if v - 1 < 0 or v > len(items):
                continue
            valid |= 1 << (v - 1)
        except ValueError:
            continue

    if exclude:
        valid ^= 2 ** (len(items).bit_length() + 1) - 1

    keys = [] 
    for item in items:
        if valid & 1:
            keys.append(item)
        valid >>= 1

    if not keys:
        return None
    
    if multiple:
        ret = []
        for key in keys:
            if key in list(menuitems.keys()):
                ret.append(key)
        return ret
    else:
        return keys[0]

def initDatabase():
    if os.path.exists("database.db"):
        if input("Database file already exists, reinitialize? [y/N]: ") in ("y", "Y"):
            try:
                os.remove("database.db")
                print("Database file deleted")
            except Exception as e:
                print("Failed to cleanup existing database file.", \
                        "Must delete manually...\n", e)
                return
        else:
            db = sqlite3.connect("database.db")
            cu = db.cursor()

            return db, cu

    db = sqlite3.connect("database.db")
    cu = db.cursor()

    try:
        with open("db/create_table.sql", "r") as f:
            cmd = ""
            for line in f.readlines():
                cmd += line
            cu.executescript(cmd)
    except Exception as e:
        print(e)

    return db, cu


def funcQueries(db, cur):
    queries = {"Select all contact information of students or teachers": queryContactInfo,
               "Select all information of wanted student or teacher": queryStudentOrTeacherInfo}

    ret = interactiveMenu(queries, multiple = False)
    if ret == None:
        return
    try:
        queries[ret](db, cur)
    except Exception as e:
        print(e)
        return


def funcRunTests(db, cur):
    subprocess.run(["tests/runtests.sh", "--exit-on-failure"])


def searchForGivenStudent(cur):
    term = input("Search student using Name and/or ID (eg. First Last, 1234): ")
    sid, name = "0", ""

    # Check for id
    for i, char in enumerate(term):
        if char in ("0123456789"):
            sid += char
        else:
            name += char

    if int(sid) == 0:
        return 0, name
    else:
        return int(sid), ""


def funcUpdateStudent(db, cur):
    studentID, studentName = searchForGivenStudent(cur)

    # Evaluate if student exists
    if len(studentName.split(" ")) != 2:
        if int(studentID) == 0:
            print("Must give either ID or both names")
            return
    else:
        first = studentName.split(" ")[0]
        last = studentName.split(" ")[1]

    query = "SELECT * FROM Student WHERE "
    query += f"student_ID = {studentID}" if studentID != 0 else \
             f"first_name = '{first}'"
    query += "" if studentID != 0 else f" AND last_name = '{last}'"
    query += ";"

    if not cur.execute(query):
        print("Student does not exist")
        return

    columns = ["Name", "Date of Birth", "Email", "Major"]

    attrs = {columns[0]: "name 'First Last'",
             columns[1]: "birthdate 'dd.mm.yyyy'",
             columns[2]: "email 'some.thing@doma.in'",
             columns[3]: "major"}

    selection = interactiveMenu(attrs)

    if not selection:
        return

    sel = []
    for i, attr in enumerate(selection):
        sel.append((attr, input(f"Enter new {attrs[attr]}: ")))

    # Sanitize and parse input
    for column, attribute in sel:
        validattr = ""
        for char in re.findall("(\s|[a-zA-Z0-9]|ä|Ä|ö|Ö|å|Å|@|\.)", attribute):
            validattr += char

        if not validattr:
            return

        if column == columns[0]: # Name
            if len(validattr.split(" ")[:50]) != 2:
                print("Must provide both first and last name, separated by space")
                return 

            newfirst = validattr.split(" ")[0][:50]
            newlast = validattr.split(" ")[1][:50]

            query =  f"UPDATE Student SET first_name = '{newfirst}', "
            query += f"last_name = '{newlast}' WHERE "
        elif column == columns[1]: # birthdate
            bday = re.search("([0-9]{2}\.){2}[0-9]{4}", validattr[:50])
            if not bday:
                return
            query = f"UPDATE Student SET date_of_birth = '{bday.string}' WHERE "
        elif column == columns[2]: # Email
            email = re.search("(\w|-|_)*\.?(\w|-|_)*@(\w|\.|-|_)*\.[a-z]*", validattr[:50])
            if not email:
                return
            query = f"""UPDATE Student SET email = "{email.string}" WHERE """
        elif column == columns[3]: # Major
            major = validattr[:50]
            query = f"UPDATE Student SET subject = '{major}' WHERE "
        else:
            print("Bad attribute")
            return

        query += f"student_ID = {studentID}" if studentID != 0 else \
                 f"first_name = '{first}' AND last_name = '{last}'"
        query += ";"

        cur.execute(query)
    
    db.commit()

    success = ""
    for i, col in enumerate(selection):
        success += f"{col}{', ' if i < len(selection) - 1 else '.'}"
    print(f"\nUpdated {success.lower()}")



def queryStudents(db, cur):
    output = cur.execute("SELECT * FROM Student;")
    for line in output:
        print(line)


def queryStudentOrTeacherInfo(db, cur):
    info = input("Do you want to print teacher or student information? [T/S]: ")
    if info == "S":
        name = input("Write the of last name the student: ")
        output = cur.execute(f"SELECT * FROM Student WHERE last_name = '{name}';").fetchall()

    elif info == "T": 
        name = input("Write the last name of the Teacher: ")
        output = cur.execute(f"SELECT * FROM Teacher WHERE last_name = '{name}';").fetchall()
    else: 
        return
    for line in output:
        print(line)

def queryContactInfo(db, cur):
    info = input("Do you want teachers or students contact information? [T/S]: ")
    if info == "S":
        output = cur.execute(f'SELECT last_name, first_name, email FROM Student;').fetchall()

    elif info == "T":
        output = cur.execute(f'SELECT last_name, first_name, email FROM Teacher;').fetchall()
    else:
        return
    for line in output:
        print(line)

def funcSearchStudent(db, cur):
    name = input("What is the last name of the student of which information you wish to search?: ")
    cur.execute(f"SELECT * FROM Student WHERE last_name = '{name}';")
    oneRow = cur.fetchone()

    if not oneRow:
        print("No such student found")
        return

    print("\nStudent ID:    " + str(oneRow[0]))
    print("Last name:     " + str(oneRow[1]))
    print("First name:    " + str(oneRow[2]))
    print("Date of birth: " + str(oneRow[3]))
    print("Email:         " + str(oneRow[4]))
    print("Subject:       " + str(oneRow[5]))

def funcDeleteStudent(db, cur):
    studentID = input("What is the id of the student to be deleted from the database?: ")

    try:
        cur.execute(f'DELETE FROM Student WHERE student_ID = {studentID};')
    except sqlite3.OperationalError as e:
        print("No such student found")
        return

    db.commit()

def funcInsertStudent(db, cur):
    try:
        id = int(input("Write the student id (xxxx): "))
    except ValueError:
        print("Invalid ID, must follow format XXXX")
        return
    bd = input("Write the date of birth (dd.mm.yyyy): ")
    email = input("Write the students email: ")
    lastname = input("Write the last name: ")
    firstname = input("Write the first name: ")
    subject = input("Write the subject: ")

    cur.execute(f"INSERT INTO Student VALUES ({id}, '{firstname}', '{lastname}', '{bd}', '{email}', '{subject}');")
    db.commit()
    return

if __name__ == "__main__":
    db, cur = initDatabase()

    while True:
        mainmenu = {"Run example queries": funcQueries,
                    "Run tests (requires bash)": funcRunTests,
                    "Search data from Student table": funcSearchStudent,
                    "Delete data from Student table": funcDeleteStudent,
                    "Insert data to Student table": funcInsertStudent,
                    "Update student information": funcUpdateStudent}

        ret = interactiveMenu(mainmenu, multiple = False)
        if ret == None:
            break

        mainmenu[ret](db, cur)

