CREATE TABLE University(
    name VARCHAR(50)
);

CREATE TABLE Teacher(
    teacher_ID INTEGER NOT NULL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL
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
    (1001, "Geoff", "Douglas", "02.05.1985"),
    (1002, "Anastasia", "Peterson", "13.05.1978"),
    (1003, "Brad", "Baron"),
    (1004, "Daniel", "Inder"),
    (1005, "Troy", "Sable", "17.04. "),
    (1006, "Jennifer", "Frawley", "16.08.1981"),
    (1007, "Monica", "Kaldor", "30.01.1989");
    