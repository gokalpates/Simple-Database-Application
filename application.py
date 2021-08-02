from sqlite3.dbapi2 import Cursor, Row, sqlite_version_info
import tkinter as tk
import sqlite3
import os
from tkinter.constants import RADIOBUTTON
from typing import Counter
from functools import partial


class Application:
    def __init__(self) -> None:
        # Create a window.
        self.root = tk.Tk()
        self.root.title("Friend Database App")

        # If database is not available then create it.
        if not os.path.exists(os.path.join(os.getcwd(), "friends.db")):
            connection = sqlite3.connect("friends.db")
            cursor = connection.cursor()
            cursor.execute("""CREATE TABLE friends (
                firstName text,
                secondName text,
                birthDate text,
                phoneNumber text
            )""")
            connection.commit()
            connection.close()

    def run(self):
        self.__createWidgets()
        self.__packWidgets()
        self.root.mainloop()

    def __createWidgets(self):
        self.firstNameLabel = tk.Label(self.root, text="First Name: ")
        self.firstNameEntry = tk.Entry(self.root, width=30)

        self.secondNameLabel = tk.Label(self.root, text="Second Name: ")
        self.secondNameEntry = tk.Entry(self.root, width=30)

        self.birthDateLabel = tk.Label(self.root, text="Birth Date: ")
        self.birthDateEntry = tk.Entry(self.root, width=30)

        self.phoneNumberLabel = tk.Label(self.root, text="Phone Number: ")
        self.phoneNumberEntry = tk.Entry(self.root, width=30)

        self.addRecordButton = tk.Button(
            self.root, text="Add Record To Database", width=50, command=self.__addRecordButton)
        self.deleteRecordButton = tk.Button(
            self.root, text="Delete Record From Database", width=50, command=self.__deleteRecordButton)
        self.showRecordButton = tk.Button(
            self.root, text="Show Records", width=50, command=self.__showRecordButton)

    def __packWidgets(self):
        self.firstNameLabel.grid(row=0, column=0)
        self.firstNameEntry.grid(row=0, column=1)

        self.secondNameLabel.grid(row=1, column=0)
        self.secondNameEntry.grid(row=1, column=1)

        self.birthDateLabel.grid(row=2, column=0)
        self.birthDateEntry.grid(row=2, column=1)

        self.phoneNumberLabel.grid(row=3, column=0)
        self.phoneNumberEntry.grid(row=3, column=1)

        self.addRecordButton.grid(row=4, column=0, columnspan=2)
        self.deleteRecordButton.grid(row=5, column=0, columnspan=2)
        self.showRecordButton.grid(row=6, column=0, columnspan=2)

    def __addRecordButton(self):
        connection = sqlite3.connect("friends.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO friends VALUES (:f_name, :s_name, :b_date, :p_number)",
                       {
                           "f_name": self.firstNameEntry.get(),
                           "s_name": self.secondNameEntry.get(),
                           "b_date": self.birthDateEntry.get(),
                           "p_number": self.phoneNumberEntry.get()
                       })
        connection.commit()
        connection.close()

        self.firstNameEntry.delete(0, tk.END)
        self.secondNameEntry.delete(0, tk.END)
        self.birthDateEntry.delete(0, tk.END)
        self.phoneNumberEntry.delete(0, tk.END)

    def __showRecordButton(self):
        connection = sqlite3.connect("friends.db")
        cursor = connection.cursor()

        cursor.execute("SELECT *, oid FROM friends")
        records = cursor.fetchall()

        window = tk.Toplevel(self.root)
        window.title("Show..")

        i, j = 0, 0
        for record in records:
            recordFrame = tk.Frame(window)
            for item in record:
                itemLabel = tk.Label(recordFrame, text=str(item), width=30)
                if i % 2 == 0:
                    itemLabel.configure(bg="orange")
                    recordFrame.configure(bg="orange")
                else:
                    itemLabel.configure(bg="white")
                    recordFrame.configure(bg="white")
                itemLabel.grid(row=i, column=j, sticky="ew")
                j += 1
            recordFrame.pack(fill=tk.X)
            j = 0
            i += 1

        window.mainloop()

        connection.commit()
        connection.close()

    def __deleteRecordButton(self):
        window = tk.Toplevel(self.root)
        window.title("Delete..")

        def deleteIdButton():
            connection = sqlite3.connect("friends.db")
            cursor = connection.cursor()

            cursor.execute("DELETE from friends WHERE oid = " +
                           str(deleteIdEntry.get()))

            connection.commit()
            connection.close()
            window.destroy()

        deleteIdLabel = tk.Label(window, text="Delete ID: ")
        deleteIdEntry = tk.Entry(window, width=30)
        deleteIdButton = tk.Button(
            window, text="Delete", command=deleteIdButton, width=50)

        deleteIdLabel.grid(row=0, column=0)
        deleteIdEntry.grid(row=0, column=1)
        deleteIdButton.grid(row=1, column=0, columnspan=2)

        window.mainloop()
