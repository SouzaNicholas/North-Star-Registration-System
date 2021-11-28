import guiWin

import sys

import sqlite3 as sql


def main():
    # Making the connection with database stuff here
    conn = sql.connect("NorthStarRegistrationDB.db")

    cursor = conn.cursor()

    app = guiWin.QApplication(sys.argv)

    ex = guiWin.Window(conn, cursor)

   # window = guiWin.Window()

    ex.isHidden()

    sys.exit(app.exec_())


main()


