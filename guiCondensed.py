import sqlite3
import sys
import objects as obj

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel, QRadioButton, QMessageBox, \
    QComboBox, QToolBox

import pandas as pd


class LookupWindow(QMainWindow):
    def __init__(self, record):
        super().__init__()
        if type(record) == obj.Student:
            self.setup_student_ui(record)
        elif type(record) == obj.Faculty:
            self.setup_faculty_ui(record)
        elif type(record) == obj.Course:
            self.setup_course_ui(record)
        elif type(record) == obj.Section:
            self.setup_section_ui(record)

    def setup_student_ui(self, student: obj.Student):
        self.setWindowTitle("Student Lookup")

        # StudentId
        self.student_label = QLabel(self)
        self.studentId = QLabel(self)
        # student Enrolled
        self.student_enrolled_label = QLabel(self)
        self.studentEnrolled = QLabel(self)

        # student credits
        self.student_credits_label = QLabel(self)
        self.studentCredits = QLabel(self)

        # Student Name
        self.student_name_label = QLabel(self)
        self.studentName = QLabel(self)
        # studentButton
        self.add_course = QPushButton(self)
        self.review = QPushButton(self)
        self.remove_course = QPushButton(self)
        self.remove_student = QPushButton(self)
        self.modify_student = QPushButton(self)
        self.print_semester = QPushButton(self)
        self.done = QPushButton(self)
        self.cancel = QPushButton(self)

        self.setGeometry(20, 20, 500, 500)
        # StudentId
        self.student_label.setText("ID:")
        self.student_label.resize(100, 30)
        self.student_label.move(20, 10)
        self.studentId.setText(student.ID)
        self.studentId.resize(150, 20)
        self.studentId.move(75, 20)

        # student Name
        self.student_name_label.setText("Name:")
        self.student_name_label.resize(100, 30)
        self.student_name_label.move(20, 55)
        self.studentName.setText(student.name)
        self.studentName.resize(150, 20)
        self.studentName.move(75, 60)
        # student enrolled
        self.student_enrolled_label.setText("Enrolled:")
        self.student_enrolled_label.resize(150,30)
        self.student_enrolled_label.move(20,95)
        self.studentEnrolled.resize(150,20)
        self.studentEnrolled.move(75,100)

        # student Credits
        self.student_credits_label.setText("Credits:")
        self.student_credits_label.resize(150,20)
        self.student_credits_label.move(20,150)
        self.studentCredits.resize(150,20)
        self.studentCredits.move(75,150)


        # student AddButton
        self.add_course.setText("Add Course")
        self.add_course.move(20, 200)
        # student review
        self.review.setText("Review")
        self.review.move(370,150)
        # student RemoveCourseButton
        self.remove_course.setText("Remove Course")
        self.remove_course.resize(150, 30)
        self.remove_course.move(20, 250)

        # student ModifyButton
        self.modify_student.setText("Modify Student")
        self.modify_student.resize(150, 30)
        self.modify_student.move(20,300)


        # student Remove Student Button
        self.remove_student.setText("Remove Student")
        self.remove_student.resize(150, 30)
        self.remove_student.move(20, 350)

        # Print Semester Registration
        self.print_semester.setText("Print Semester Registration")
        self.print_semester.resize(300,30)
        self.print_semester.move(20,400)



        # student doneButton
        self.done.setText("Done")
        self.done.move(20, 450)
        self.done.clicked.connect(self.done_exit)

        # student cancelButton
        self.cancel.setText("Cancel")
        self.cancel.resize(100, 30)
        self.cancel.move(270, 450)

    def setup_faculty_ui(self, faculty: obj.Faculty):
        self.setWindowTitle("Faculty Lookup")

        # facultyId
        self.faculty_label = QLabel(self)
        self.facultyId = QLabel(self)

        # facultyName
        self.faculty_name_label = QLabel(self)
        self.facultyName = QLabel(self)
        # facultyButton
        self.add_course = QPushButton(self)
        self.remove_course = QPushButton(self)
        self.remove_faculty = QPushButton(self)
        self.done = QPushButton(self)
        self.cancel = QPushButton(self)

        self.setGeometry(20, 20, 500, 500)
         # facultyId
        self.faculty_label.setText("ID")
        self.faculty_label.resize(100, 30)
        self.faculty_label.move(20, 10)
        self.facultyId.setText(faculty.ID)
        self.facultyId.resize(150,20)
        self.facultyId.move(67,20)

        # faculty Name
        self.faculty_name_label.setText("Name")
        self.faculty_name_label.resize(100,30)
        self.faculty_name_label.move(20,55)
        self.facultyName.setText(faculty.name)
        self.facultyName.resize(150,20)
        self.facultyName.move(67,60)

        # faculty AddButton
        self.add_course.setText("Add Course")
        self.add_course.move(20,100)

        # faculty RemoveCourseButton
        self.remove_course.setText("Remove Course")
        self.remove_course.resize(150,30)
        self.remove_course.move(20,150)

        # faculty RemoveEmployeeButton
        self.remove_faculty.setText("Remove Faculty")
        self.remove_faculty.resize(150,30)
        self.remove_faculty.move(20,200)

        # faculty doneButton
        self.done.setText("Done")
        self.done.move(20,350)
        self.done.clicked.connect(self.done_exit)

        # faculty cancelButton
        self.cancel.setText("Cancel")
        self.cancel.resize(100,30)
        self.cancel.move(270, 350)

    def setup_course_ui(self, course: obj.Course):
        self.setWindowTitle("Course Lookup")

        # courseId
        self.course_label = QLabel(self)
        self.courseId = QLabel(self)

        # courseDescription
        self.course_description_label = QLabel(self)
        self.courseDescription = QLabel(self)

        # courseCredits
        self.course_credits_label = QLabel(self)
        self.courseCredits = QLabel(self)

        # courseButton
        self.remove_course = QPushButton(self)
        self.done = QPushButton(self)
        self.cancel = QPushButton(self)
        self.print_semester = QPushButton(self)

        self.setGeometry(20, 20, 400, 400)
        # courseId
        self.course_label.setText("ID")
        self.course_label.resize(100, 30)
        self.course_label.move(20, 10)
        self.courseId.setText(course.course_ID)
        self.courseId.resize(150, 20)
        self.courseId.move(100, 20)

        # course Description
        self.course_description_label.setText("Description:")
        self.course_description_label.resize(150, 30)
        self.course_description_label.move(20, 45)
        self.courseDescription.setText(course.name)
        self.courseDescription.resize(150, 20)
        self.courseDescription.move(100, 50)

        self.course_credits_label.setText("Credits:")
        self.course_credits_label.resize(100, 30)
        self.course_credits_label.move(20, 95)
        self.courseCredits.setText(str(course.credits))
        self.courseCredits.resize(150, 20)
        self.courseCredits.move(100, 100)

        # course RemoveCourseButton
        self.remove_course.setText("Remove Course")
        self.remove_course.resize(150, 30)
        self.remove_course.move(20, 150)

        # Print Registration

        self.print_semester.setText("Print Semester Registration")
        self.print_semester.resize(300, 30)
        self.print_semester.move(20, 300)

        # course doneButton
        self.done.setText("Done")
        self.done.move(20, 350)
        self.done.clicked.connect(self.done_exit)

        # course cancelButton
        self.cancel.setText("Cancel")
        self.cancel.resize(100, 30)
        self.cancel.move(270, 350)

    def setup_section_ui(self, section: obj.Section):
        course = obj.Course(section.course_ID)
        self.setWindowTitle("Course Section Lookup")

        # SectionId
        self.section_id_label = QLabel(self)
        self.sectionId = QLabel(self)

        # section Description
        self.section_description_label = QLabel(self)
        self.sectionDescription = QLabel(self)

        # section
        self.section_name_label = QLabel(self)
        self.sectionName = QLabel(self)

        # section credits
        self.section_credits_label = QLabel(self)
        self.sectionCredits = QLabel(self)

        # section capacity
        self.section_capacity_label = QLabel(self)
        self.sectionCapacity = QLabel(self)

        # section semester
        self.section_semester_label = QLabel(self)
        self.sectionSemester = QLabel(self)


        # section Button
        self.review = QPushButton(self)
        self.remove_section = QPushButton(self)
        self.print_semester = QPushButton(self)
        self.done = QPushButton(self)
        self.cancel = QPushButton(self)

        self.setGeometry(20, 20, 600, 600)
        # SectionId
        self.section_id_label.setText("ID:")
        self.section_id_label.resize(100, 30)
        self.section_id_label.move(20, 10)
        self.sectionId.setText(str(section.section_ID))
        self.sectionId.resize(150, 20)
        self.sectionId.move(100, 20)

        # section Description
        self.section_description_label.setText("Description:")
        self.section_description_label.resize(100, 30)
        self.section_description_label.move(20, 55)
        self.sectionDescription.setText(course.name)
        self.sectionDescription.resize(150, 20)
        self.sectionDescription.move(100, 60)

        # section
        self.section_name_label.setText("Section:")
        self.section_name_label.resize(150, 30)
        self.section_name_label.move(20, 95)
        self.sectionName.setText("00" + str(section.section_ID))
        self.sectionName.resize(150, 20)
        self.sectionName.move(100, 100)

        # section Credits
        self.section_credits_label.setText("Credits:")
        self.section_credits_label.resize(150, 20)
        self.section_credits_label.move(20, 150)
        self.sectionCredits.setText(str(course.credits))
        self.sectionCredits.resize(150, 20)
        self.sectionCredits.move(100, 150)


        # section Capacity
        self.section_capacity_label.setText("Capacity:")
        self.section_capacity_label.resize(150, 20)
        self.section_capacity_label.move(20, 250)
        self.sectionCapacity.setText(str(section.capacity))
        self.sectionCapacity.resize(150, 20)
        self.sectionCapacity.move(100, 250)

        # section Semester
        self.section_semester_label.setText("Semester:")
        self.section_semester_label.resize(150, 20)
        self.section_semester_label.move(20,300)
        self.sectionSemester.setText(section.semester)
        self.sectionSemester.resize(150, 20)
        self.sectionSemester.move(100, 300)

        # section review
        self.review.setText("Review")
        self.review.move(450, 250)
        # section Remove
        self.remove_section.setText("Remove section")
        self.remove_section.resize(150, 30)
        self.remove_section.move(20, 350)

        # Print Semester Registration
        self.print_semester.setText("Print Semester Registration")
        self.print_semester.resize(300, 30)
        self.print_semester.move(20, 500)

        # student doneButton
        self.done.setText("Done")
        self.done.move(20, 550)
        self.done.clicked.connect(self.done_exit)

        # student cancelButton
        self.cancel.setText("Cancel")
        self.cancel.resize(100, 30)
        self.cancel.move(450, 550)


    def done_exit(self):
        choice = QMessageBox.question(self, 'Extract!', "Are you sure ?",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Ok have a good day!")
            sys.exit()
        else:
            pass

class MainWindow(QMainWindow):
    def __init__(self, conn: sqlite3.Connection, curs: sqlite3.Cursor):
        super().__init__()
        # Labels
        self.title = 'Database'
        # creating a textfield label
        self.studentID_Label = QLabel(self)
        # creating a box to enter student Id
        self.studentID = QLineEdit(self)
        # creating a student Name Label
        self.studentName_label = QLabel(self)
        # creating a box to enter student name
        self.studentName = QLineEdit(self)

        # creating add button label
        self.add_button = QPushButton(self)

        # lookupButton
        self.lookup_button = QPushButton(self)

        # Done Button
        self.done_button = QPushButton(self)

        # This is the Error contain message if the add doesn't exist
        self.id_error = QMessageBox(self)
        self.id_error.setWindowTitle("invalid ID error")
        self.id_error.setText(" Invalid student ID. Please try again")
        # dropdown
        self.box = QComboBox(self)
        # Database tools
        self.cursor = curs
        self.connection = conn

        # setting gui
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Main Database Window")
        self.setGeometry(30, 30, 500, 500)

        # student Id field
        self.studentID_Label.setText("            Enter ID:")
        self.studentID_Label.resize(700, 125)
        self.studentID.move(30, 80)
        self.studentID.resize(150, 30)

        # student name field
        self.studentName_label.setText("          Enter name:")
        self.studentName_label.resize(700, 270)
        self.studentName.move(30, 150)
        self.studentName.resize(150, 30)

        # will show our add button inside Main Window
        self.add_button.resize(70, 30)
        self.add_button.move(20, 200)
        self.add_button.setText('Add')
        self.add_button.clicked.connect(self.add_button_connection)

        # LookUp Button
        self.lookup_button.resize(100, 30)
        self.lookup_button.move(100, 200)
        self.lookup_button.setText('Lookup')
        self.lookup_button.clicked.connect(self.build_lookup)

        # Done Button
        self.done_button.resize(100, 30)
        self.done_button.move(350, 200)
        self.done_button.setText("Done")
        self.done_button.clicked.connect(self.done_exit)

        # dropDown
        # self.box.resize(100,50)
        self.box.move(30, 10)
        self.box.addItem("Student")
        self.box.addItem("Course")
        self.box.addItem("Faculty")
        self.box.addItem("Section")

        # show on the display
        self.show()

    def done_exit(self):
        choice = QMessageBox.question(self, 'Extract!', "Are you sure ?",
                              QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
         print("Ok have a good day!")
         sys.exit()
        else:
            pass

    def add_button_connection(self):
        # connection with the enrolment table
        # the joint
        table = 'enrollment'
        # self.StudentID.text() will  get the string out the text box and store it into the studentID
        studentID = self.studentID.text()
        # this method will check if the studentID exist and it will return a boolean value either 0 or one
        query = f"""SELECT EXISTS(SELECT 1 FROM Enrollment WHERE studentID ='{studentID}')"""
        flag = self.cursor.execute(query).fetchall()[0][0]
        if flag == 1:  # this line will check if the student is there it will print the information
            # print(studentID) Here I am missing the student name and course description because we did not specify
            # it in our database table The student database table only have name instead of the student name and same
            # with the course table
            query = f"""SELECT Enrollment.studentID, S.Name, c.Name, sectionID, flag FROM
                   Enrollment INNER JOIN Student S on S.studentID = Enrollment.studentID
                   INNER JOIN Section sec on sec.sectionID= sectionID
                   INNER JOIN course c on sec.courseID= c.courseID WHERE Enrollment.studentID= '{studentID}'"""
            self.cursor.execute(query)
            fence = pd.DataFrame.from_records(self.cursor.fetchall())
            print(fence)
        else:
            self.id_error.exec()

    def build_lookup(self):
        record_type = self.box.currentText()
        record = None
        if record_type == "Student":
            record = obj.Student(self.studentID.text())
        elif record_type == "Faculty":
            record = obj.Faculty(self.studentID.text())
        elif record_type == "Course":
            record = obj.Course(self.studentID.text())
        elif record_type == "Section":
            record = obj.Section(self.studentID.text())
        self.lookup = LookupWindow(record)
        self.lookup.show()
