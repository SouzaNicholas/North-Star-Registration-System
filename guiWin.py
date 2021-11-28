import sqlite3

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel, QRadioButton, QMessageBox

import pandas as pd


# want to open window2
class Window2(QMainWindow):
    def __init__(self):
        super.__init__()
        self.setWindowTitle("LookUp Table")


class Window(QMainWindow):

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

        # Database tools
        self.cursor = curs
        self.connection = conn

        # setting gui
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Main Database Window")
        self.setGeometry(30, 30, 500, 500)

        # student Id field
        self.studentID_Label.setText("            Enter student ID:")
        self.studentID_Label.resize(700, 50)
        self.studentID.move(30, 40)
        self.studentID.resize(150, 30)

        # student name field
        self.studentName_label.setText("          Enter student name:")
        self.studentName_label.resize(700, 200)
        self.studentName.move(30, 120)
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
        self.lookup_button.clicked.connect(self.window2)

        # Done Button
        self.done_button.resize(100, 30)
        self.done_button.move(350, 200)
        self.done_button.setText("Done")

        # show on the display
        self.show()

    # window2
    def window2(self):
        self.open_new_window = Window2()
        # print("Table")
        self.open_new_window.show()

        # this method will make our button function respond when we click it

    def add_button_connection(self):
        # connection with the enrolment table

        #the joint

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
            query = f"""SELECT Enrollment.studentID, sectionID, flag FROM
                   Enrollment INNER JOIN Student S on S.studentID = Enrollment.studentID
                   INNER JOIN Section sec on sec.sectionID= sectionID
                   INNER JOIN course c on sec.courseID= c.courseID WHERE Enrollment.studentID= '{studentID}'"""

            self.cursor.execute(query)
            fence = pd.DataFrame.from_records(self.cursor.fetchall())
            print(fence)

        else:

            self.id_error.exec()
