import sqlite3 as sql


class Student:

    def __init__(self, ID: str, name: str):
        self.ID = ID
        self.name = name

    def add(self, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""INSERT INTO Student (StudentID, Name) VALUES (?, ?)""", (self.ID, self.name))
        except Exception as e:
            # Display message in GUI along the lines of "Unexpected error occured. Try again."
            print("placeholder")
        conn.commit()

    def remove(self, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""DELETE FROM Enrollment WHERE 
                                EXISTS (SELECT * FROM Enrollment WHERE StudentID = (?))""", self.ID)
            cursor.execute("""DELETE FROM Student WHERE StudentID = (?)""", self.ID)
        except Exception as e:
            # Display error message in GUI similar to "Student not found in DB"
            print("placeholder")
        conn.commit()

    def modify(self, name, cursor: sql.Cursor, conn: sql.Connection):
        self.name = name
        try:
            cursor.execute("""UPDATE Student SET Name=(?) WHERE StudentID=(?)""", (self.name, self.ID))
        except Exception as e:
            # Display message in GUI along the lines of "Unexpected error occured. Try again."
            print("placeholder")
        conn.commit()

    def add_course(self, ID: str, course_section_ID:str, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""INSERT INTO Enrollment (No., StudentID, Course_SectionID, Flag) VALUES (default, ?, ?, ?)""",
                       (ID, course_section_ID, 0))  # Passes default to No., as it's auto incremented
        except Exception as e:
            # Display message in GUI along the lines of "Unexpected error occured. Try again."
            print("placeholder")
        conn.commit()

    def remove_course(self, course_section_ID: str, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""DELETE FROM Enrollment WHERE EXISTS 
                      (SELECT * FROM Enrollment WHERE StudentID = (?) AND COURSE_SECTIONID = (?))""",
                       (self.ID, course_section_ID))
        except Exception as e:
            # Display message in GUI along the lines of "Unexpected error occured. Try again."
            print("placeholder")
        conn.commit()

    def check_flags(self, cursor: sql.Cursor, conn: sql.Connection) -> bool:
        #SQL call to total credits among course sections
        #return total > limit
        return False


class Faculty:

    def __init__(self, ID: str, name: str):
        self.ID = ID
        self.name = name

    def add(self, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""INSERT INTO Faculty (FacultyID, Name) VALUES (?, ?)""", (self.ID, self.name))
        except Exception as e:
            # Display message in GUI along the lines of "Unexpected error occured. Try again."
            print("placeholder")
        conn.commit()

    def remove(self, cursor: sql.Cursor, conn: sql.Connection):
        # Must be implemented in such a way that it checks Section to make sure
        # The faculty member has no dependencies. If so, the record will be deleted
        # Will revisit later -NS
        conn.commit()

    def modify(self, name: str, cursor: sql.Cursor, conn: sql.Connection):
        self.name = name
        try:
            cursor.execute("""UPDATE Faculty SET Name=(?) WHERE FacultyID=(?)""", (self.name, self.ID))
        except Exception as e:
            # Display message in GUI along the lines of "Unexpected error occured. Try again."
            print("placeholder")
        conn.commit()

    def add_course(self, course_section_ID:str, cursor: sql.Cursor, conn: sql.Connection):
        try:
            cursor.execute("""UPDATE Section SET FacultyID=(?) WHERE Course_SectionID=(?)""", (self.ID, course_section_ID))
        except Exception as e:
            # Display message in GUI along the lines of "Unexpected error occured. Try again."
            print("placeholder")
        conn.commit()

    def remove_course(self, ID: str, courseID: str, cursor: sql.Cursor, conn: sql.Connection):
        # This method may need to be removed. To remove faculty from a course section,
        # FacultyID in that section would have to be changed. The only way to do that is
        # by setting it to null or inserting a new Faculty ID. Since FacultyID is
        # non-nullable and it doesn't make sense to pass in the ID of a different
        # faculty member, I think the safest bet is to cut this. -NS
        conn.commit()


class Course:
    id: str
    description: str
    credits: int

    def remove(self, cursor: sql.Cursor, conn: sql.Connection):
        print("remove_course")

    def add(self, cursor: sql.Cursor, conn: sql.Connection):
        print("add_course")


class Section:
    section_ID: str
    course_ID: str
    instructor: str
    capacity: int

    def add(self, cursor: sql.Cursor, conn: sql.Connection):
        print("add_section")

    def remove(self, cursor: sql.Cursor, conn: sql.Connection):
        print("remove_section")

    def check_flags(self, cursor: sql.Cursor, conn: sql.Connection) -> bool:
        print("check_flags")
        return False

    def print_class_list(self, cursor: sql.Cursor, conn: sql.Connection):
        print("print_class_list")
