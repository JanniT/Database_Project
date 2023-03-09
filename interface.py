#!/usr/bin/python3

import sqlite3
import subprocess
import sys
import os


def interactiveMenu(menuitems: dict, prompt: str = "Select",
        exclude: bool = False, multiple: bool = True):
    items = list(menuitems.keys())
    
    print(f"{prompt}:\n")
    for i, item in enumerate(items):
        print(f"\t{i + 1}: {item}")
    print("\n\t0: Cancel\n")

    strInclude = f"""{"exclude" if exclude else "include"}"""
    strMultiple = f"""Select one{' or multiple (eg: "1", "1 4 2")' if multiple else ''}"""

    indices = input(f"""Items to {strInclude}. {strMultiple}\n : """).split(" ")
    
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

    ret = [] 
    for item in items:
        if valid & 1:
            ret.append(item)
        valid >>= 1
    
    if not ret:
        return None

    ret = ret if multiple else ret[0]

    if ret not in list(menuitems.keys()):
        return None

    return ret

def initDatabase():
    if os.path.exists("database.db"):
        try:
            os.remove("database.db")
        except Exception as e:
            print("Failed to cleanup existing database file.", \
                    "Must delete manually...\n", e)
            return

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

    return cu


def funcQueries(cur):
    queries = {"Select all from Student table": queryStudents}

    ret = interactiveMenu(queries, multiple = False)
    if ret == None:
        return
    
    try:
        queries[ret](cur)
    except Exception as e:
        print(e)
        return

def funcRunTests(cur):
    subprocess.run(["tests/runtests.sh", "--exit-on-failure"])

def queryStudents(cur):
    output = cur.execute("SELECT * FROM Student;")
    for line in output:
        print(line)

def queryStudentOrTeacherInfo(cur):

    info = input("Do you want to print teacher or student information? [T/S]: ")
    if info == "S":
        name = input("Write the of last name the student: ")
        cur.execute(f'SELECT * FROM Student WHERE last_name = {name};')

    elif info == "T": 
        name = input("Write the last name of the Teacher: ")
        cur.execute(f'SELECT * FROM Teacher WHERE last_name = {name};')
    else: 
        return

def queryContactInfo(cur):
    
    info = input("Do you want teachers or students contact information? [T/S]: ")
    if info == "S":
        cur.execute(f'SELECT last_name, first_name, email FROM Student;')

    elif info == "T":
        cur.execute(f'SELECT last_name, first_name, email FROM Teacher;')
    else:
        return

def funcSearchStudent(cur):
    name = input("What is the last name of the student of which information you wish to search?: ")
    cur.execute(f'SELECT * FROM Student WHERE {name};')
    oneRow = cur.fetchone()

    print("Student ID: " + str(oneRow['student_ID']))
    print("Last name: " + str(oneRow['last_name']))
    print("First name: " + str(oneRow['first_name']))
    print("Date of birth: " + str(oneRow['date_of_birth']))
    print("Email: " + str(oneRow['email']))
    print("Subject: " + str(oneRow['subject']))
    return

def funcDeleteStudent(cur):
    studentID = input("What is the last name of the student to be deleted from the database?: ")
    cur.execute(f'DELETE FROM Student WHERE student_ID = {};')
    
    return


if __name__ == "__main__":
    cur = initDatabase()

    while True:
        mainmenu = {"Run example queries": funcQueries,
                    "Run tests (requires bash)": funcRunTests}

        ret = interactiveMenu(mainmenu, multiple = False)
        if ret == None:
            break

        mainmenu[ret](cur)

