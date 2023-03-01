CREATE TABLE University(
    name VARCHAR(50) NOT NULL, 
    FOREIGN KEY (student_id)
        REFERENCES Student (student_id),
    FOREIGN KEY(teacher_id)
        REFERENCES Teacher (teacher_id)
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