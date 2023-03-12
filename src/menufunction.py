import subprocess
import sqlite3
import re

import queries as q
import util

# Interactive menu where one can choose what queries to run
def funcQueries(db, cur):
    queries = {"Select all contact information of students or teachers":
               q.queryContactInfo,
               "Select all information of wanted student or teacher":
               q.queryStudentOrTeacherInfo,
               "List classes for all or given student":
               q.queryStudentClasses,
               "List work projects of all/given student":
               q.queryStudentWorkProject,
               "List teachers from selected university":
               q.queryGetTeachers}

    ret = util.interactiveMenu(queries, prompt="Examples", multiple=False)
    if ret is None:
        return
    try:
        queries[ret](db, cur)
    except Exception as e:
        print(e)
        return


def funcRunTests(db, cur):
    subprocess.run(["tests/runtests.sh", "--exit-on-failure"])

# This function is horrible, do not look at it
def funcUpdateStudent(db, cur):
    studentID = util.searchForGivenStudent(cur)

    if not studentID:
        return

    columns = ["Name", "Date of Birth", "Email", "Major"]

    attrs = {columns[0]: "name 'First Last'",
             columns[1]: "birthdate 'dd.mm.yyyy'",
             columns[2]: "email 'some.thing@doma.in'",
             columns[3]: "major"}

    selection = util.interactiveMenu(attrs)

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

        if column == columns[0]:  # Name
            if len(validattr.split(" ")[:50]) != 2:
                print("Must provide first and last name separated by space")
                return

            newfirst = validattr.split(" ")[0][:50]
            newlast = validattr.split(" ")[1][:50]

            query = f"UPDATE Student SET first_name = '{newfirst}', "
            query += f"last_name = '{newlast}' WHERE "
        elif column == columns[1]:  # Birthdate
            bd = re.search("([0-9]{2}\.){2}[0-9]{4}", validattr[:50])
            if not bd:
                return
            query = f"UPDATE Student SET date_of_birth = '{bd.string}' WHERE "
        elif column == columns[2]:  # Email
            email = re.search("(\w|-|_)*\.?(\w|-|_)*@(\w|\.|-|_)*\.[a-z]*",
                              validattr[:50])
            if not email:
                return
            query = f"""UPDATE Student SET email = "{email.string}" WHERE """
        elif column == columns[3]:  # Major
            major = validattr[:50]
            query = f"UPDATE Student SET subject = '{major}' WHERE "
        else:
            print("Bad attribute")
            return

        query += f"student_ID = {studentID};"

        cur.execute(query)

    db.commit()

    # Print which columns changes were done eg.
    # "Updated name, email, major."
    success = ""
    for i, col in enumerate(selection):
        success += f"{col}{', ' if i < len(selection) - 1 else '.'}"
    print(f"\nUpdated {success.lower()}")


def funcSearchStudent(db, cur):
    name = input("Last name of the student: ")
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
    studentID = input("ID of the student to be deleted from the database: ")

    try:
        cur.execute(f'DELETE FROM Student WHERE student_ID = {studentID};')
    except sqlite3.OperationalError:
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
    university = input("Write the university: ")

    query = "INSERT INTO Student VALUES"
    query += f"({id}, '{firstname}', '{lastname}', '{bd}', '{email}',"
    query += f"'{subject}', '{university}');"

    cur.execute(query)
    db.commit()
