import sqlite3
import subprocess

def menu(items: list) -> int:
    print("\nSelect one:\n")
    for i, item in enumerate(items):
        print(f"\t{i + 1}. {item}")
    print("\n\t0. Exit")

    
    selection = input(" : ")
    valid = ""

    for char in selection:
        if char in ("0123456789"):
            valid += char
    
    ret = int(valid) - 1
    return -1 if ret < 0 or ret > len(items) - 1 else ret

if __name__ == "__main__":
    running = True
    while running:
        s = menu(["Query 1", "Query 2", "Query 3", "Query 4", "Query 5"])
        running = (s != -1)
        print(s)

