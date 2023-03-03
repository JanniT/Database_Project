#!/usr/bin/python3
import sys
import sqlite3

if __name__ == "__main__":
    try:
        db = sqlite3.connect("test_database.db")
        cu = db.cursor()

        output = cu.execute("SELECT * FROM Project;").fetchall()

        if len(output) != 5:
            print("Incorrect amount of rows in table")
            exit(1) 

    except Exception as e:
        print(e)
        exit(1)



