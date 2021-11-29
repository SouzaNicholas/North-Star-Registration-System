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
    def add_course(self, course_section_ID:str, cursor: sql.Cursor, conn: sql.Connection):
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

    # TODO: This requires a complicated series of SQL calls that I will return to. -NS
    def check_flags(self, cursor: sql.Cursor, conn: sql.Connection) -> bool:
        # SQL call to find credit value of student's courses
        cursor.execute("""""")
        #return total > limit
        return False


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
    # TODO: This method is currently able to insert IDs of faculty members that do not exist. Will fix. -NS
    def add_course(self, course_section_ID:str, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""UPDATE Section SET FacultyID=(?) WHERE Course_SectionID=(?)""",
                           (self.ID, course_section_ID))
        except Exception as e:
            # Display message in GUI along the lines of "Unexpected error occured. Try again."
            print("Failed to add faculty to course for:", self.ID)
        conn.commit()

    def remove_course(self, ID: str, courseID: str, cursor: sql.Cursor, conn: sql.Connection):
        # This method may need to be removed. To remove faculty from a course section,
        # FacultyID in that section would have to be changed. The only way to do that is
        # by setting it to null or inserting a new Faculty ID. Since FacultyID is
        # non-nullable and it doesn't make sense to pass in the ID of a different
        # faculty member, I think the safest bet is to cut this. -NS
        conn.commit()


class Course:

    def __init__(self, id: str, name: str, credits: int):
        self.id = id
        self.name = name
        self.credits = int

    def add(self, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""INSERT INTO Course (CourseID, Name, Credits) VALUES (?, ?, ?);""",
                           (self.id, self.name, self.credits))
        except Exception as e:
            print("failed to add course to 'Course'")
        conn.commit()

    # TODO: is course safe to delete? Check section, student, or faculty first? -BG
    def remove(self, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""DELETE FROM Course WHERE CourseID=(?);""", (self.id,))
        except Exception as e:
            print("failed to remove course from 'Course'")
        conn.commit()


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

    # TODO:
    def remove(self, cursor: sql.Cursor, conn: sql.Connection):
        pass

    # TODO:
    def check_flags(self, cursor: sql.Cursor, conn: sql.Connection) -> bool:
        print("check_flags")
        return False

    def print_class_list(self, cursor: sql.Cursor, conn: sql.Connection):
        try:
            print("print_class_list")
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
