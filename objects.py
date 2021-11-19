import sqlite3


class Student:

    def __init__(self, ID: str, name: str):
        self.ID = ID
        self.name = name

    def add(self):
        #SQL call to add record to DB
        #try:
        #   cursor.execute("""INSERT INTO student (ID, name) VALUES (?, ?)""", (self.ID, self.name))
        #except Exception as e:
        #   TODO(Figure out what exception you'd get here)
        print()

    def remove(self):
        #SQL call to remove record to DB
        #try
        #   cursor.execute()
        #except Exception as e:
        #   TODO(Figure out what exception you'd get here)
        print()

    def modify(self, name):
        self.name = name
        #SQL call to update record
        print()

    def add_course(self, ID: str, courseID:str):
        #SQL call to create enrollment record
        print()


    def remove_course(self, ID: str, courseID: str):
        #SQL call to delete enrollment record
        print()

    def check_flags(self) -> bool:
        #SQL call to total credits among course sections
        #return total > limit
        return False


class Faculty:

    def __init__(self, ID: str, name: str):
        self.ID = ID
        self.name = name

    def add(self):
        # SQL call to add record to DB
        print()

    def remove(self):
        #SQL call to remove record to DB
        print()

    def modify(self, name: str):
        self.name = name
        #SQL call to update record
        print()

    def add_course(self, ID: str, courseID:str):
        #SQL call to create enrollment record
        print()

    def remove_course(self, ID: str, courseID: str):
        #SQL call to delete enrollment record
        print()


class Course:
    id: str
    description: str
    credits: int

    def remove(self):
        print("remove_course")

    def add(self):
        print("add_course")


class Section:
    section_ID: str
    course_ID: str
    instructor: str
    capacity: int

    def add(self):
        print("add_section")

    def remove(self):
        print("remove_section")

    def check_flags(self) -> bool:
        print("check_flags")
        return False

    def print_class_list(self):
        print("print_class_list")
