#!/usr/bin/python3

import sqlite3
import subprocess
import sys



def interactiveMenu(menuitems: dict, prompt: str = "Select", exclude: bool = False, multiple: bool = True):
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

    return (db, cu)

def funcQueries():

    db, cu = initDatabase()

    queries = {"Select all from University table": "SELECT * FROM University;",
               "Select all from Student table": "SELECT * FROM Student;"}

    ret = interactiveMenu(queries, multiple = False)
    if ret == None:
        return
    
    try:
        out = cu.execute(queries[ret]).fetchall()
    except Exception as e:
        print(e)
        return

    print(f"\nSuccess!\n")
    for line in out:
        print(line)
    print("")

def funcRunTests():
    subprocess.run(["tests/runtests.sh", "--exit-on-failure"])

def funcDummy():
    print("Jeerock")

if __name__ == "__main__":
    while True:
        mainmenu = {"Run example queries": funcQueries,
                    "Run tests": funcRunTests}

        ret = interactiveMenu(mainmenu, multiple = False)
        if ret == None:
            break

        mainmenu[ret]()

