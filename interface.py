#!/usr/bin/python3

import sqlite3
import sys
import os

sys.path.append("src/")

import menufunction as menu
import util


def initDatabase():
    if os.path.exists("database.db"):
        if input("Database file already exists, reinitialize? [y/N]: ") \
                in ("y", "Y"):
            try:
                os.remove("database.db")
                print("Database file deleted")
            except Exception as e:
                print("Failed to cleanup existing database file.",
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


if __name__ == "__main__":
    db, cur = initDatabase()

    while True:
        mainmenu = {"Run example queries": menu.funcQueries,
                    "Run tests (requires bash)": menu.funcRunTests,
                    "Search data from Student table": menu.funcSearchStudent,
                    "Delete data from Student table": menu.funcDeleteStudent,
                    "Insert data to Student table": menu.funcInsertStudent,
                    "Update student information": menu.funcUpdateStudent}

        ret = util.interactiveMenu(mainmenu, prompt="Main menu", multiple=False)
        if ret is None:
            break

        mainmenu[ret](db, cur)
