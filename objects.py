import sqlite3 as sql


class Student:

    def __init__(self, ID: str, name: str):
        self.ID = ID
        self.name = name

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
    def remove(self, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""DELETE FROM Enrollment WHERE StudentID=(?)""", [self.ID])
        except Exception as e:
            print("Could not delete enrollments for", self.ID)
        try:
            cursor.execute("""DELETE FROM Student WHERE StudentID = (?)""", [self.ID])
        except Exception as e:
            print("remove failed to finish for", self.ID)
        conn.commit()

    # Updates the student's record with the provided name.
    def modify(self, name, cursor: sql.Cursor, conn: sql.Connection):
        self.name = name
        try:
            cursor.execute("""UPDATE Student SET Name=(?) WHERE StudentID=(?)""", (self.name, self.ID))
        except Exception as e:
            print("failed to modify student")
        conn.commit()

    # Creates an enrollment record linking this student to the provided seciton record
    def add_course(self, course_section_ID: str, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""INSERT INTO Enrollment (StudentID, Course_SectionID, Flag) VALUES (?, ?, ?)""",
                           (self.ID, course_section_ID, 0))  # Passes nothing to EnrollmentID, as it's auto incremented
        except Exception as e:
            print("Could not add course")
        conn.commit()

    # Deletes an enrollment record connecting this student and the provided section.
    def remove_course(self, course_section_ID: str, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""DELETE FROM Enrollment WHERE StudentID = (?) AND COURSE_SECTIONID = (?)""",
                           (self.ID, course_section_ID))
        except Exception as e:
            print("Could not remove course")
        conn.commit()

    def check_flags(self, cursor: sql.Cursor) -> bool:
        credits = 0
        cursor.execute("""SELECT Course.Credits FROM Course JOIN Section, Enrollment, Student 
                        WHERE Course.CourseID = Section.CourseID
                        AND Section.Course_SectionID = Enrollment.Course_SectionID
                        AND Student.StudentID = Enrollment.StudentID
                        AND Enrollment.StudentID = (?)""", [self.ID])
        for i in cursor.fetchall():
            credits += i[0]

        if credits > 12:
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

    def __init__(self, ID: str, name: str):
        self.ID = ID
        self.name = name

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
    def remove(self, cursor: sql.Cursor, conn: sql.Connection):
        cursor.execute("""SELECT * FROM Section WHERE FacultyID = (?)""", [self.ID])
        if len(cursor.fetchall()) < 1:
            try:
                cursor.execute("""DELETE FROM Faculty WHERE FacultyID = (?) AND FacultyID = (?)""", (self.ID, self.ID))
            except Exception as e:
                # Display error message in GUI similar to "Student not found in DB"
                print("remove failed to finish for", self.ID)
        else:
            print("Could not delete faculty. Remove from current courses.")
        conn.commit()

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
        try:
            cursor.execute("""UPDATE Section SET FacultyID=(?) WHERE Course_SectionID=(?)""",
                           ("00000000", course_section_ID))
        except Exception as e:
            # Display message in GUI along the lines of "Unexpected error occured. Try again."
            print("Failed to remove faculty from course for:", self.ID)
        conn.commit()


class Course:

    def __init__(self, id: str, name: str, credits: int):
        self.id = id
        self.name = name
        self.credits = credits

    def add(self, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""INSERT INTO Course (CourseID, Name, Credits) VALUES (?, ?, ?);""",
                           (self.id, self.name, self.credits))
        except Exception as e:
            print("failed to add course to 'Course'")
        conn.commit()

    # checks if sections still exist, if not then safe to delete. -BG
    def remove(self, cursor: sql.Cursor, conn: sql.Connection):
        cursor.execute("""SELECT * FROM Section WHERE CourseID=(?)""", [self.id])
        if len(cursor.fetchall()) < 1:
            try:
                cursor.execute("""DELETE FROM Course WHERE CourseID=(?);""", (self.id,))
            except Exception as e:
                print("failed to remove course from 'Course'")
        else:
            print("Could not delete course. Try removing associated sections first.")
        conn.commit()


# TODO: Check for misinputs. If type in wrong info on object creation says has been removed even tho there is no section
class Section:

    def __init__(self, course_section_ID: str, course_ID: str, faculty_ID: str, section_ID: int, capacity: int,
                 semester: str):
        self.course_section_ID = course_section_ID
        self.course_ID = course_ID
        self.faculty_ID = faculty_ID
        self.section_ID = section_ID
        self.capacity = capacity
        self.semester = semester

    def add(self, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""INSERT INTO Section (Course_SectionID, CourseID, FacultyID, SectionID, Capacity, 
            Semester) VALUES (?, ?, ?, ?, ?, ?);""", (self.course_section_ID, self.course_ID, self.faculty_ID,
                                                      self.section_ID, self.capacity, self.semester))
        except Exception as e:
            print("failed to add section to 'Section'")
        conn.commit()

    def remove(self, cursor: sql.Cursor, conn: sql.Connection):
        cursor.execute("""SELECT * FROM Enrollment WHERE Course_SectionID=(?)""", [self.course_section_ID])
        if len(cursor.fetchall()) < 1:
            try:
                cursor.execute("""DELETE FROM Section WHERE Course_SectionID=(?);""", (self.course_section_ID,))
            except Exception as e:
                print("failed to remove Section")
        else:
            print("Could not delete Section.")
        conn.commit()

    # TODO:
    def check_flags(self, cursor: sql.Cursor, conn: sql.Connection) -> bool:
        capacity = 0
        # find total capacity
        cursor.execute("""""")

        # check course section max capacity
        cursor.execute("""SELECT * FROM Section WHERE Course_SectionID='(?)'""", (self.course_section_ID,))
        fetch = cursor.fetchone()
        # print(fetch)
        step = 0
        for i in fetch:
            step += 1
            if step == 5:
                # print(i)
                max_capacity = i
        if capacity > max_capacity:
            return True
        else:
            return False

    # TODO:
    def print_class_list(self, cursor: sql.Cursor, conn: sql.Connection):
        try:
            # get studentID from enrollment if course_sectionID matches
            cursor.execute("""SELECT * Enrollment WHERE course_sectionID='(?)'""", (self.course_section_ID,))
            # get name of students with id from 'Student' -BG
            id_list = cursor.fetchall()
            for i in id_list:
                cursor.execute("""SELECT * Student WHERE StudentID='(?)'""", (i,))
                print(cursor.fetchone())
        except Exception as e:
            print("failed to print class list")
        conn.commit()
