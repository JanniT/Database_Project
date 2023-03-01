import sqlite3
import subprocess
import sys

def menu(allItems: dict) -> str:
    items = list(allItems.keys())

    print("\nSelect one:\n")
    for i, item in enumerate(items):
        print(f"\t{i + 1}. {item}")
    print("\n\t0. Exit")

    
    selection = input(" : ")
    valid = ""

    for char in selection:
        if char in ("0123456789"):
            valid += char
    
    try:
        ret = int(valid) - 1
    except ValueError:
        return ""

    if ret < 0 or ret > len(items) - 1:
        return ""

    if ret == -1:
        sys.exit()

    return allItems[items[ret]] if items[ret] in list(allItems.keys()) else ""

if __name__ == "__main__":
    running = True
    while running:
        queries = {"Select all from uni": "SELECT * FROM University;",
                   "Select all from jee": "SELECT * FROM Jee;",
                   "Prööt": "Jeejee jee rock rock :DDDDD"
                   }

        print(menu(queries))

