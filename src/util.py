def interactiveMenu(menuitems: dict, prompt: str = "Select",
                    exclude: bool = False, multiple: bool = True):
    items = list(menuitems.keys())

    print(f"\n{prompt}:\n")
    for i, item in enumerate(items):
        print(f"\t{i + 1}: {item}")
    print("\n\t0: Cancel\n")

    strMultiple = f"""Select one{' or multiple (eg: "1", "1 4 2")'
                                 if multiple else ''}"""

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


def searchForGivenStudent(cur) -> int:
    term = input("Search student via Name and/or ID (eg. First Last, 1234): ")
    sid, name = "0", ""

    # Check for id
    for i, char in enumerate(term):
        if char in ("0123456789"):
            sid += char
        else:
            name += char

    query = "SELECT * FROM Student "

    if int(sid) == 0:
        if len(name.split(" ")) != 2:
            print("Invalid name")
            return

        first = name.split(" ")[0][:50]
        last = name.split(" ")[1][:50]
        query += f"WHERE first_name = '{first}' AND last_name = '{last}';"
    else:
        query += f"WHERE student_ID = {sid}"

    out = cur.execute(query)
    if not out:
        print("Student does not exist")
        return None

    return int(out.fetchall()[0][0])
