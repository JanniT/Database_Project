CREATE TABLE University(
    name VARCHAR(50) NOT NULL,
    student_ID INTEGER,
    teacher_ID INTEGER,
    FOREIGN KEY (student_ID)
        REFERENCES Student (student_ID),
    FOREIGN KEY(teacher_ID)
        REFERENCES Teacher (teacher_ID),
    UNIQUE (student_ID, teacher_ID)
);

CREATE TABLE Teacher(
    teacher_ID INTEGER NOT NULL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    class_name VARCHAR(50),
    CHECK (teacher_ID > 0),
    FOREIGN KEY (class_name)
        REFERENCES Class (name)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    UNIQUE (teacher_ID, email)
);

CREATE TABLE Class(
    room_ID INTEGER DEFAULT 0000 PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    student_ID INTEGER,
    teacher_ID INTEGER,
    FOREIGN KEY (student_ID)
        REFERENCES Student (student_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (teacher_ID)
        REFERENCES Teacher (teacher_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    UNIQUE (student_ID, teacher_ID)
);

CREATE TABLE Student(
    student_ID INTEGER NOT NULL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    subject VARCHAR(50) NOT NULL,
    
    UNIQUE (student_ID, email)
);

-- Student data 
INSERT INTO Student VALUES
    (9321, "Jofa", "Kaiffari", "01.01.1999", "jofa.kaiffari@jeerock.com", "Software Engineering"),
    (9829, "Iskender", "Kebab", "04.03.2001", "iskender.kebab@jeerock.com", "Software Engineering"),
    (3376, "Big", "Mac", "19.11.2000", "big.mac@jeerock.com", "Industrial Engineering and Management"),
    (1659, "Pepsi", "Man", "30.01.2000", "pepsi.man@jeerock.com", "Industrial Engineering and Management"),
    (5548, "Albert", "Einstein", "12.08.1999", "albert.einstein@jeerock.com", "Computational Engineering"),
    (9863, "Helsinki", "City", "02.02.2002", "helsinki.city@jeerock.com", "Environmental Engineering"),
    (7593, "Schrödingering", "Kissa", "01.01.1999", "jofa.kaiffari@jeerock.com", "Computational Engineering");


--Insering text to the table
INSERT INTO University (name) VALUES
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
    
--Inserting stuff to Class table
INSERT INTO Class (room_ID, name, student_ID, teacher_ID) VALUES
    (1, "Data Structures and Algorithms", 9321, 1001),
    (2, "Basics of Database Systems", 9829, 1002),
    (3, "Svenska i Arbetslivet", 3376, 1003),
    (4, "Introduction to DevOps", 1659, 1004),
    (5, "Discrete Models and Methods", 5548, 1005),
    (6, "Basics of Linux", 9863, 1006),
    (7, "Foundations of Computer Science", 7593, 1007);
