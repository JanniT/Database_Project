CREATE TABLE University(
    name VARCHAR(50) NOT NULL,
    student_ID INTEGER,
    teacher_ID INTEGER,
    class_name varchar(50),
    FOREIGN KEY (student_ID)
        REFERENCES Student (student_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY(teacher_ID)
        REFERENCES Teacher (teacher_ID)
        ON UPDATE CASCADE 
        ON DELETE CASCADE,
    FOREIGN KEY(class_name)
        REFERENCES Class (name)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    UNIQUE (student_ID, teacher_ID)
);

CREATE TABLE Teacher(
    teacher_ID INTEGER NOT NULL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    class_name VARCHAR(50),
    university_name VARCHAR(50),
    CHECK (teacher_ID > 0),
    FOREIGN KEY (class_name)
        REFERENCES Class (name)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (university_name)
        REFERENCES University (name)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    UNIQUE (teacher_ID, email)
);

CREATE TABLE Class(
    name VARCHAR(50) NOT NULL PRIMARY KEY,
    room_ID INTEGER DEFAULT 0000,
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
    university_name VARCHAR(50) NOT NULL,
    FOREIGN KEY (university_name)
        REFERENCES University (name)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    UNIQUE (student_ID, email)
);

CREATE TABLE Company(
    company_name VARCHAR(50) NOT NULL,
    student_ID INTEGER NOT NULL,
    project_ID INTEGER NOT NULL,
    FOREIGN KEY (student_ID)
        REFERENCES Student (student_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (project_ID)
        REFERENCES Project (project_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Project(
    project_ID INTEGER NOT NULL PRIMARY KEY,
    project_name VARCHAR(50) NOT NULL,
    student_ID INTEGER NOT NULL,
    FOREIGN KEY (student_ID)
        REFERENCES Student (student_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE INDEX student_name_alphabetical ON Student (last_name, first_name);

CREATE INDEX project_name_alphabetical ON Project (project_name ASC);

-- Dummy data for Project table
INSERT INTO Project VALUES
    (1234, "Backlog grooming", 9321),
    (1235, "Script improvements", 9829),
    (1236, "Solve DaVinci Code", 7593),
    (1237, "Wabble hands", 1659),
    (1238, "Complete time dialation formulas", 5548);

-- Dummy data for Company table
INSERT INTO Company VALUES
    ("Ballpit startup", 9321, 1234),
    ("International Multibillion Megacorporation", 9829, 1235),
    ("Illuminati", 7593, 1236),
    ("Chocolate Factory", 1659, 1237),
    ("Physics Institute", 5548, 1238);

-- Student data 
INSERT INTO Student VALUES
    (9321, "Jofa", "Kaiffari", "01.01.1999", "jofa.kaiffari@jeerock.com", "Software Engineering", "LUT University"),
    (9829, "Iskender", "Kebab", "04.03.2001", "iskender.kebab@jeerock.com", "Software Engineering", "LUT University"),
    (3376, "Big", "Mac", "19.11.2000", "big.mac@jeerock.com", "Industrial Engineering and Management", "LUT University"),
    (1659, "Pepsi", "Man", "30.01.2000", "pepsi.man@jeerock.com", "Industrial Engineering and Management", "LUT University"),
    (5548, "Albert", "Einstein", "12.08.1999", "albert.einstein@jeerock.com", "Computational Engineering", "LUT University"),
    (9863, "Helsinki", "City", "02.02.2002", "helsinki.city@jeerock.com", "Environmental Engineering", "LUT University"),
    (7593, "Schrödingering", "Kissa", "01.01.1999", "jofa.kaiffari@jeerock.com", "Computational Engineering", "LUT University");


--Insering text to the table
INSERT INTO University (name) VALUES
    ("LUT University"),
    ("Aalto University"),
    ("University of Oulu"),
    ("University of Vaasa"),
    ("University of Eastern Finland");

--Inserting stuff to the Teacher table
INSERT INTO Teacher VALUES
    (1001, "Geoff", "Douglas", "02.05.1985", "geoff.douglas@jeejee.fi", "Data Struectures and Algorithms", "LUT University"),
    (1002, "Anastasia", "Peterson", "13.05.1978", "anastasia.peterson@jeejee.fi", "Basics of Database Systems", "LUT University"),
    (1003, "Brad", "Baron","12.12.1986", "brad.barond@jeejee.fi", "Svenska i Arbetslivet", "LUT University"),
    (1004, "Daniel", "Inder", "09.09.1967", "daniel.inder@jeejee.fi", "Introduction to DevOps", "LUT University"),
    (1005, "Troy", "Sable", "17.04.1988", "troy.sable@jeejee.fi", "Discrete Models and Methods", "LUT University"),
    (1006, "Jennifer", "Frawley", "16.08.1981", "jennifer.frawley@jeejee.fi", "Basics of Linux", "LUT University"),
    (1007, "Monica", "Kardashian", "30.01.1989", "monica.kaldor@jeejee.fi", "Foundation of Computer Science", "Aalto University"),

    (2001, "Jay", "Weyney", "17.12.1967", "jay.Weyney@jeejee.fi", "Basics of Database Systems", "Aalto University"),
    (2002, "Dominic", "Partson", "19.08.1985", "dominic.partson@jeejee.fi", "Foundation of Computer Science", "Aalto University"),
    (2003, "Hayden", "Way", "27.06.1975", "hayden.Way@jeejee.fi", "Svenska i Arbetslivet", "Aalto University"),
    (2004, "Jack", "Jackson", "26.02.1973", "jay.jackson@jeejee.fi", "Discrete Models and Methods", "Aalto University"),

    (3001, "Ye", "West", "26.06.1969", "ye.west@jeejee.fi", "Foundation of Computer Science", "University of Oulu"),
    (3002, "Michael", "Jackson", "06.08.1975", "michael.jackson@jeejee.fi", "Basics of Database Systems", "University of Oulu"),
    (3003, "Cashey", "Hayday", "18.01.1976", "cashey.hayday@jeejee.fi", "Basics of Linux", "University of Oulu"),
    (3004, "Liam", "Sheesh", "26.02.1973", "liam.sheesh@jeejee.fi", "Foundation of Computer Science", "University of Oulu"),

    (4001, "Kal", "Bin", "17.12.1958", "kal.bin@jeejee.fi", "Foundation of Computer Science", "University of Vaasa"),
    (4002, "Frederick", "Daylight", "18.03.1978", "frederick.daylight@jeejee.fi", "Basics of Database Systems", "University of Vaasa"),
    (4003, "Ocland", "mesh", "18.12.1968", "ocland.mesh@jeejee.fi", "Svenska i Arbetslivet", "University of Vaasa"),
    (4004, "Penelope", "Hay", "20.09.1992", "penelope.hay@jeejee.fi", "Discrete Models and Methods", "University of Vaasa"),

    (5001, "frank", "pert", "01.01.1990", "frank.pert@jeejee.fi", "Svenska i Arbetslivet", "University of Eastern Finland"),
    (5002, "Akon", "Lind", "18.08.1986", "akon.lind@jeejee.fi", "Discrete Models and Methods", "University of Eastern Finland"),
    (5003, "Joshua", "Jayd", "16.12.1995", "joshua.jayd@jeejee.fi", "Basics of Database Systems", "University of Eastern Finland"),
    (5004, "Jen", "Pol", "02.01.1985", "jen.pol@jeejee.fi", "Foundation of Computer Science", "University of Eastern Finland");
    
--Inserting stuff to Class table
INSERT INTO Class (name, room_ID, student_ID, teacher_ID) VALUES
    ("Data Structures and Algorithms", 1, 9321, 1001),
    ("Basics of Database Systems", 2, 9829, 1002),
    ("Svenska i Arbetslivet", 3, 3376, 1003),
    ("Introduction to DevOps", 4, 1659, 1004),
    ("Discrete Models and Methods", 5, 5548, 1005),
    ("Basics of Linux", 6, 9863, 1006),
    ("Foundations of Computer Science", 7, 7593, 1007);

