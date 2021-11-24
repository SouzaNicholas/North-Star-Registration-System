import sqlite3 as sql


class Student:

    def __init__(self, ID: str, name: str):
        self.ID = ID
        self.name = name

    def add(self, cursor: sql.Cursor, conn: sql.Connection):
        cursor.execute("""INSERT INTO student (ID, name) VALUES (?, ?)""", (self.ID, self.name))
        conn.commit()

    def remove(self, cursor: sql.Cursor, conn: sql.Connection):
        #SQL call to remove record to DB
        #try
        #   cursor.execute()
        #except Exception as e:
        #   TODO(Figure out what exception you'd get here)
        print()

    def modify(self, name, cursor: sql.Cursor, conn: sql.Connection):
        self.name = name
        #SQL call to update record
        print()

    def add_course(self, ID: str, courseID:str, cursor: sql.Cursor, conn: sql.Connection):
        #SQL call to create enrollment record
        print()


    def remove_course(self, ID: str, courseID: str, cursor: sql.Cursor, conn: sql.Connection):
        #SQL call to delete enrollment record
        print()

    def check_flags(self, cursor: sql.Cursor, conn: sql.Connection) -> bool:
        #SQL call to total credits among course sections
        #return total > limit
        return False


class Faculty:

    def __init__(self, ID: str, name: str):
        self.ID = ID
        self.name = name

    def add(self, cursor: sql.Cursor, conn: sql.Connection):
        # SQL call to add record to DB
        print()

    def remove(self, cursor: sql.Cursor, conn: sql.Connection):
        #SQL call to remove record to DB
        print()

    def modify(self, name: str, cursor: sql.Cursor, conn: sql.Connection):
        self.name = name
        #SQL call to update record
        print()

    def add_course(self, ID: str, courseID:str, cursor: sql.Cursor, conn: sql.Connection):
        #SQL call to create enrollment record
        print()

    def remove_course(self, ID: str, courseID: str, cursor: sql.Cursor, conn: sql.Connection):
        #SQL call to delete enrollment record
        print()


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
