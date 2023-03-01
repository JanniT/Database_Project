CREATE TABLE University(
    name VARCHAR(50) NOT NULL,
    student_ID INTEGER NOT NULL,
    teacher_ID INTEGER NOT NULL,
    FOREIGN KEY (student_ID)
        REFERENCES Student (student_ID),
    FOREIGN KEY(teacher_ID)
        REFERENCES Teacher (teacher_ID)
);

--Insering text to the table
INSERT INTO University (name) VALUES
    ("LUT University"),
    ("Aalto University"),
    ("University of Oulu"),
    ("University of Vaasa"),
    ("University of Eastern Finland");