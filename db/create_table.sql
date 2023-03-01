CREATE TABLE University(
    name VARCHAR(50) NOT NULL, 
    FOREIGN KEY (student_id)
        REFERENCES Student (student_id),
    FOREIGN KEY(teacher_id)
        REFERENCES Teacher (teacher_id)
);

CREATE TABLE Teacher(
    teacher_ID INTEGER NOT NULL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    CHECK (teacher_ID > 0),
    UNIQUE (teacher_ID, email)
);

CREATE TABLE Student(
    

);

--Insering text to the table
INSERT INTO University VALUES
    ("LUT University"),
    ("Aalto University"),
    ("University of Oulu"),
    ("University of Vaasa"),
    ("University of Eastern Finland");

--Inserting stuff to the Teacher table
INSERT INTO Teacher VALUES
    (1001, "Geoff", "Douglas", "02.05.1985", "geoff.douglas@jeejee.fi"),
    (1002, "Anastasia", "Peterson", "13.05.1978", "anastasia.peterson@jeejee.fi"),
    (1003, "Brad", "Baron","12.12.1986", "brad.barond@jeejee.fi"),
    (1004, "Daniel", "Inder", "09.09.1967", "daniel.inder@jeejee.fi"),
    (1005, "Troy", "Sable", "17.04.1988", "troy.sable@jeejee.fi"),
    (1006, "Jennifer", "Frawley", "16.08.1981", "jennifer.frawley@jeejee.fi"),
    (1007, "Monica", "Kaldor", "30.01.1989", "monica.kaldor@jeejee.fi");
    