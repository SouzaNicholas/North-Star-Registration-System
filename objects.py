import sqlite3 as sql


class Student:
    def __init__(self, parameters: list[str]):
        conn = sql.connect("NorthStarRegistrationDB.db")
        curs = conn.cursor()
        curs.execute("SELECT * FROM Student WHERE StudentID = (?)", [parameters[0]])
        record = curs.fetchone()

        # Checks to see if the query returned anything.
        # If not, we assume this is a new record.
        # Therefore, the parameters passed in must have the
        # rest of the information a new record would need
        if record is not None:
            self.ID = record[0]
            self.name = record[1]
        elif len(parameters) >= 2:
            self.ID = parameters[0]
            self.name = parameters[1]
        self.credits = self.credits(curs)
        conn.close()

    # Adds this student to the database
    def add(self, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""INSERT INTO Student (StudentID, Name) VALUES (?, ?);""", (self.ID, self.name))
        except Exception as e:
            print("add failed to finish")
        conn.commit()

    # When only one value is needed, string must be passed as a list.
    # Otherwise, it will be interpreted as a sequence of character inputs.
    # For example, passing "00001234" will be taken as 8 inputs
    def remove(self, cursor: sql.Cursor, conn: sql.Connection) -> bool:
        try:
            cursor.execute("""DELETE FROM Enrollment WHERE StudentID=(?)""", [self.ID])
        except Exception as e:
            print("Could not delete enrollments for", self.ID)
        try:
            cursor.execute("""DELETE FROM Student WHERE StudentID = (?)""", [self.ID])
        except Exception as e:
            print("remove failed to finish for", self.ID)
        conn.commit()
        return True

    # Updates the student's record with the provided name.
    def modify(self, name, cursor: sql.Cursor, conn: sql.Connection):
        self.name = name
        try:
            cursor.execute("""UPDATE Student SET Name=(?) WHERE StudentID=(?)""", (self.name, self.ID))
        except Exception as e:
            print("failed to modify student")
        conn.commit()

    # Creates an enrollment record linking this student to the provided section record

    def add_course(self, course_section_ID: str, cursor: sql.Cursor, conn: sql.Connection):
        flag = 0  # default value of flag is 0, indicating no issue.
        try:
            cursor.execute("""INSERT INTO Enrollment (StudentID, Course_SectionID, Flag) VALUES (?, ?, ?)""",
                           (self.ID, course_section_ID, 0))  # Passes nothing to EnrollmentID, as it's auto incremented
            if self.check_flags(cursor):
                flag = 1
                cursor.execute("""UPDATE Enrollment SET Flag = (?) WHERE StudentID = (?)
                                AND Course_SectionID = (?)""", (flag, self.ID, course_section_ID))
        except Exception as e:
            print("Could not add course")
        conn.commit()

    # Deletes an enrollment record connecting this student and the provided section.
    def remove_course(self, course_section_ID: str, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""DELETE FROM Enrollment WHERE StudentID = (?) AND COURSE_SECTIONID = (?)""",
                           (self.ID, course_section_ID))
            if not self.check_flags(cursor):
                flag = 0
                cursor.execute("""UPDATE Enrollment SET Flag = (?) WHERE StudentID = (?)""",
                               (flag, self.ID, course_section_ID))
        except Exception as e:
            print("Could not remove course")
        conn.commit()

    def credits(self, cursor: sql.Cursor) -> int:
        cred = 0
        cursor.execute("""SELECT Course.Credits FROM Course JOIN Section, Enrollment, Student 
                                WHERE Course.CourseID = Section.CourseID
                                AND Section.Course_SectionID = Enrollment.Course_SectionID
                                AND Student.StudentID = Enrollment.StudentID
                                AND Enrollment.StudentID = (?)""", [self.ID])
        for i in cursor.fetchall():
            cred += i[0]
        return cred

    def check_flags(self, cursor: sql.Cursor) -> bool:
        if self.credits(cursor) > 12:
            return True
        else:
            return False

    def print_registration(self, cursor: sql.Cursor):
        cursor.execute("""SELECT Section.Course_SectionID, Course.Name, Course.Credits FROM Course JOIN Section, Student, Enrollment
                        WHERE Section.Course_SectionID = Enrollment.Course_SectionID
                        AND Course.CourseID = Section.CourseID
                        AND Student.StudentID = Enrollment.StudentID
                        AND Student.StudentID = (?)""", [self.ID])
        return cursor.fetchall()


class Faculty:
    def __init__(self, parameters: list[str]):
        conn = sql.connect("NorthStarRegistrationDB.db")
        curs = conn.cursor()
        try:
            curs.execute("""SELECT * FROM Faculty WHERE FacultyID = (?)""", [parameters[0]])
        except Exception as e:
            print("Could not fetch record")
        record = curs.fetchone()

        # Checks to see if the query returned anything.
        # If not, we assume this is a new record.
        # Therefore, the parameters passed in must have the
        # rest of the information a new record would need
        if record is not None:
            self.ID = record[0]
            self.name = record[1]
        elif len(parameters) >= 2:
            self.ID = parameters[0]
            self.name = parameters[1]
        conn.close()

    # Adds the faculty record to the database.
    def add(self, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""INSERT INTO Faculty (FacultyID, Name) VALUES (?, ?)""", (self.ID, self.name))
        except Exception as e:
            # Display message in GUI along the lines of "Unexpected error occured. Try again."
            print("Failed to add faculty")
        conn.commit()

    # Checks to make sure the faculty member is not teaching any courses.
    # If they are not, they will be removed form the database.
    def remove(self, cursor: sql.Cursor, conn: sql.Connection) -> bool:
        cursor.execute("""SELECT * FROM Section WHERE FacultyID = (?)""", [self.ID])
        if len(cursor.fetchall()) > 0:
            try:
                cursor.execute("""DELETE FROM Faculty WHERE FacultyID = (?) AND FacultyID = (?)""", (self.ID, self.ID))
            except Exception as e:
                # Display error message in GUI similar to "Student not found in DB"
                print("remove failed to finish for", self.ID)
            conn.commit()
            return True
        else:
            print("Could not delete faculty. Remove from current courses.")
            return False

    # Updates a faculty record with the provided name.
    def modify(self, name: str, cursor: sql.Cursor, conn: sql.Connection):
        self.name = name
        try:
            cursor.execute("""UPDATE Faculty SET Name=(?) WHERE FacultyID=(?)""", (self.name, self.ID))
        except Exception as e:
            # Display message in GUI along the lines of "Unexpected error occured. Try again."
            print("Failed to update faculty:", self.ID)
        conn.commit()

    # Changes the listed faculty ID on the provided Section record.
    def add_course(self, course_section_ID: str, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""UPDATE Section SET FacultyID=(?) WHERE Course_SectionID=(?)""",
                           (self.ID, course_section_ID))
        except Exception as e:
            # Display message in GUI along the lines of "Unexpected error occured. Try again."
            print("Failed to add faculty to course for:", self.ID)
        conn.commit()

    # Removes a faculty member from a course by changing the listed instructor
    # to a default "No Faculty" entry.
    def remove_course(self, course_section_ID: str, cursor: sql.Cursor, conn: sql.Connection):
        cursor.execute("""SELECT * FROM Section WHERE FacultyID = (?) 
                       AND Course_SectionID = (?)""", (self.ID, course_section_ID))
        sections = cursor.fetchall()
        if len(sections) > 0:
            try:
                cursor.execute("""UPDATE Section SET FacultyID=(?) WHERE Course_SectionID=(?)""",
                               ("00000000", course_section_ID))
            except Exception as e:
                # Display message in GUI along the lines of "Unexpected error occured. Try again."
                print("Failed to remove faculty from course for:", self.ID)
        conn.commit()


class Course:
    def __init__(self, parameters: list[str]):
        conn = sql.connect("NorthStarRegistrationDB.db")
        curs = conn.cursor()
        try:
            curs.execute("""SELECT * FROM Course WHERE CourseID = (?)""", [parameters[0]])
        except Exception as e:
            print("Could not fetch record")
        record = curs.fetchone()

        # Checks to see if the query returned anything.
        # If not, we assume this is a new record.
        # Therefore, the parameters passed in must have the
        # rest of the information a new record would need
        if record is not None:
            self.course_ID = record[0]
            self.name = record[1]
            self.credits = record[2]
        elif len(parameters) >= 3:
            self.course_ID = parameters[0]
            self.name = parameters[1]
            self.credits = parameters[2]
        conn.close()
        # self.id = id
        # self.name = name
        # self.credits = credits

    def add(self, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""INSERT INTO Course (CourseID, Name, Credits) VALUES (?, ?, ?);""",
                           (self.course_ID, self.name, self.credits))
        except Exception as e:
            print("failed to add course to 'Course'")
        conn.commit()

    # checks if sections still exist, if not then safe to delete. -BG
    def remove(self, cursor: sql.Cursor, conn: sql.Connection) -> bool:
        cursor.execute("""SELECT * FROM Section WHERE CourseID=(?)""", [self.course_ID])
        # if there are no sections of the course:
        if len(cursor.fetchall()) < 1:
            try:
                cursor.execute("""DELETE FROM Course WHERE CourseID=(?);""", (self.course_ID,))
            except Exception as e:
                print("failed to remove course from 'Course'")
            conn.commit()
            return True
        else:
            print("Could not delete course. Try removing associated sections first.")
            return False


class Section:
    def __init__(self, parameters: list[str]):
        conn = sql.connect("NorthStarRegistrationDB.db")
        curs = conn.cursor()
        try:
            curs.execute("""SELECT * FROM Section WHERE Course_SectionID = (?)""", [parameters[0]])
        except Exception as e:
            print("Could not fetch record")
        record = curs.fetchone()

        # Checks to see if the query returned anything.
        # If not, we assume this is a new record.
        # Therefore, the parameters passed in must have the
        # rest of the information a new record would need
        if record is not None:
            self.ID = record[0]
            self.course_ID = record[1]
            self.faculty_ID = record[2]
            self.section_ID = record[3]
            self.capacity = record[4]
            self.semester = record[5]
        elif len(parameters) >= 6:
            self.ID = parameters[0]
            self.course_ID = parameters[1]
            self.faculty_ID = parameters[2]
            self.section_ID = parameters[3]
            self.capacity = parameters[4]
            self.semester = parameters[5]
        conn.close()
        # self.course_section_ID = course_section_ID
        # self.course_ID = course_ID
        # self.faculty_ID = faculty_ID
        # self.section_ID = section_ID
        # self.capacity = capacity
        # self.semester = semester

    def add(self, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""INSERT INTO Section (Course_SectionID, CourseID, FacultyID, SectionID, Capacity, 
            Semester) VALUES (?, ?, ?, ?, ?, ?);""", (self.ID, self.course_ID, self.faculty_ID,
                                                      self.section_ID, self.capacity, self.semester))
        except Exception as e:
            print("failed to add section to 'Section'")
        conn.commit()

    def remove(self, cursor: sql.Cursor, conn: sql.Connection) -> bool:
        cursor.execute("""SELECT * FROM Enrollment WHERE Course_SectionID=(?)""", [self.ID])
        # if there are no course sections in enrollment:
        if len(cursor.fetchall()) < 1:
            try:
                cursor.execute("""DELETE FROM Section WHERE Course_SectionID=(?);""", (self.ID,))
            except Exception as e:
                print("failed to remove Section")
            conn.commit()
            return True
        else:
            print("Could not delete Section.")
            return False

    def check_flags(self, cursor: sql.Cursor, conn: sql.Connection) -> bool:
        # SELECT * FROM Enrollment WHERE Course_SectionID='ART281-001'
        cursor.execute("""SELECT * FROM Enrollment WHERE Course_SectionID=(?)""", (self.ID,))
        # enrolled = number of students taking the course section
        enrolled = cursor.fetchall()
        # SELECT * FROM Section WHERE Course_SectionID='ART281-001'
        cursor.execute("""SELECT * FROM Section WHERE Course_SectionID=(?)""", (self.ID,))
        # Capacity_check = used to find max_capacity in a section
        capacity_check = cursor.fetchall()
        # inc = incrementer
        inc = 0
        for i in capacity_check:
            for j in i:
                inc += 1
                # finds capacity column
                if inc == 5:
                    max_capacity = j
        capacity = len(enrolled)
        if capacity > max_capacity:
            return True
        else:
            return False

    def print_class_list(self, cursor: sql.Cursor):
        # get studentID from enrollment if course_sectionID matches
        cursor.execute("""SELECT Enrollment.StudentID, Student.Name FROM Enrollment JOIN Student WHERE 
                              Student.StudentID = Enrollment.StudentID AND Enrollment.Course_SectionID = (?)""",
                       [self.ID])
        return cursor.fetchall()
