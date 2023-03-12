import util

# The functionality and the purpose of these functions are documented
# in the PFD in 'doc/' directory


def queryStudentClasses(db, cur):
    all = input("Search for specific student? [y/N]: ") in ("y", "Y")

    if all:
        studentID = util.searchForGivenStudent(cur)
        if not studentID:
            return

    query = "SELECT Student.student_ID, Student.first_name, Student.last_name,"
    query += " Class.name "
    query += "FROM Student "
    query += "INNER JOIN Class "
    query += "ON Class.student_ID = Student.student_ID "
    query += ";" if not all else f"WHERE Student.student_ID = {studentID}"

    classes = cur.execute(query)
    for i in classes:
        print(i)


def queryStudentWorkProject(db, cur):
    all = input("Search for specific student? [y/N]: ") in ("y", "Y")

    if all:
        studentID = util.searchForGivenStudent(cur)
        if not studentID:
            return

    query = "SELECT DISTINCT Student.student_ID, Student.first_name, "
    query += "Student.last_name, Company.company_name, Project.project_ID, "
    query += "Project.project_name "
    query += "FROM Student "
    query += "INNER JOIN Project ON Company.project_ID = Project.project_ID "
    query += "INNER JOIN Company ON Student.student_ID = Company.student_ID "
    query += " " if not all else f"WHERE Student.student_ID = {studentID} "
    query += "GROUP BY Company.company_name;"

    projects = cur.execute(query)
    for i in projects:
        print(i)


def queryGetTeachers(db, cur):
    unicur = cur.execute("SELECT * FROM University;").fetchall()

    # Create dict with uni names as keys, values don't matter here, so are
    # assigned as None
    unis = {}
    for uni in unicur:
        unis[uni[0]] = None

    sel = util.interactiveMenu(unis, prompt="Universities", multiple=True)

    if not sel:
        return

    # For each selected uni, print separately query data from them
    for uni in sel:
        query = "SELECT * FROM Teacher"
        query += f" WHERE university_name = '{uni}';"
        o = cur.execute(query)

        for teacher in o.fetchall():
            print(teacher)


def queryStudentOrTeacherInfo(db, cur):
    info = input("Print teacher or student information? [t/s]: ")

    if info in ("S", "s"):
        name = input("Write the of last name the student: ")
        query = f"SELECT * FROM Student WHERE last_name = '{name}';"
        output = cur.execute(query).fetchall()
    elif info in ("T", "t"):
        name = input("Write the last name of the Teacher: ")
        query = f"SELECT * FROM Teacher WHERE last_name = '{name}';"
        output = cur.execute(query).fetchall()
    else:
        return

    for line in output:
        print(line)


def queryContactInfo(db, cur):
    info = input("Do you want teachers' or students' information? [t/s]: ")

    if info in ("S", "s"):
        query = "SELECT last_name, first_name, email FROM Student;"
        output = cur.execute(query).fetchall()
    elif info in ("T", "t"):
        query = "SELECT last_name, first_name, email FROM Teacher;"
        output = cur.execute(query).fetchall()
    else:
        return

    for line in output:
        print(line)
