# Menu function where a dictionary is passed, and it's keys are the menu items.
# Function supports:
#  - Selecting multiple items
#  - Inverting selection
#
# Return value will depend on if multiple item selecion is enabled.
def interactiveMenu(menuitems: dict, prompt: str = "Select",
                    exclude: bool = False, multiple: bool = True):
    items = list(menuitems.keys())

    print(f"\n{prompt}:\n")
    for i, item in enumerate(items):
        print(f"\t{i + 1}: {item}")
    print("\n\t0: Cancel\n")

    # Prompt either 'Select one' or 'Select multiple'
    strMultiple = f"""Select one{' or multiple (eg: "1", "1 4 2")'
                                 if multiple else ''}"""

    # Split user input into tokens from spaces
    indices = input(f"""{strMultiple}\n : """).split(" ")

    # Save the selected number(s) as bits, like:
    #     v third option selected
    # 0 0 1 0 1
    #         ^ first option selected
    valid = 0x0
    for i in indices:
        try:
            v = int(i)
            if v - 1 < 0 or v > len(items):
                continue
            valid |= 1 << (v - 1)
        except ValueError:
            continue

    # Invert bits if invert is enabled
    if exclude:
        valid ^= 2 ** (len(items).bit_length() + 1) - 1

    # Validate bits, see if in range and append to keys
    keys = []
    for item in items:
        if valid & 1:
            keys.append(item)
        valid >>= 1

    # If no valid keys exists, exit
    if not keys:
        return None

    # Return value. If multiple enabled, return list of valid keys.
    #               If not, return the first selection
    if multiple:
        ret = []
        for key in keys:
            if key in list(menuitems.keys()):
                ret.append(key)
        return ret
    else:
        return keys[0]


# Helper function to search and validate if a student exists.
# If does, return their studentID, if not return None
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

    # If not given ID and name doesnt consist of first and last name, return
    if int(sid) == 0:
        if len(name.split(" ")) != 2:
            print("Invalid name")
            return

        # Split name from space to first and last name
        first = name.split(" ")[0][:50]
        last = name.split(" ")[1][:50]
        query += f"WHERE first_name = '{first}' AND last_name = '{last}';"
    else:
        query += f"WHERE student_ID = {sid}"

    out = cur.execute(query)
    if not out:
        print("Student does not exist")
        return None

    # Return the student ID as integer
    return int(out.fetchall()[0][0])
