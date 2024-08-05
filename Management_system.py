# -*- coding: utf-8 -*-
"""
Created on Mon Aug 05 16:40 2024

Scout Management System

@author: Jack Rawlinson
"""
import tkinter as tk
import mysql.connector


class managment_window:
    def __init__(self):

        mydb = mysql.connector.connect(host="localhost", user="root",
                                       password="[D1x1e2021&D@isy2022]", database="scout_database")

        self.mycursor = mydb.cursor()

        self.window = tk.Tk()
        self.window.title("Scout Management")
        self.window.config(bg="#a000e4")

        self.create_entry = tk.Button(
            self.window, text="Create New Entry", command=self.create_entry)
        #self.create_entry.pack(pady=20, side=tk.LEFT)
        self.create_entry.grid(row=1, column=1, rowspan=2, columnspan=3)
        self.show_entries = tk.Button(self.window, text="Show Entries", command=self.show_entries)
        #self.show_entries.pack(pady=20, side=tk.LEFT)
        self.show_entries.grid(row=1, column=4, rowspan=2, columnspan=3)
        self.window.mainloop()

    def create_entry(self):

        self.mycursor.execute("DESCRIBE scouts_1")
        row_position = 3
        column_position = 1

        for col in self.mycursor:
            tk.Label(text=col[0]).grid(row=row_position, column=column_position, columnspan=3)
            tk.Entry(self.window, justify="center").grid(
                row=row_position+1, column=column_position, columnspan=3)  # .pack(pady=20, side=tk.BOTTOM)
            column_position += 3
        # self.window.update()
        print("In create entry")

    def show_entries(self):
        print("In show entries")


mydb = mysql.connector.connect(host="localhost", user="root",
                               password="[D1x1e2021&D@isy2022]", database="scout_database")

mycursor = mydb.cursor()

# mycursor.execute(
#    "ALTER TABLE scouts ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
#sql = "INSERT INTO scouts_1 (name, Guardian1, Guardian1_contact, Guardian2) VALUES (%s, %s,%s, %s,%s)"
#val = (('John', 'mum', 'mum_contact', 'dad', 'dad_contact'))
#mycursor.execute(sql, val)
mycursor.execute("SHOW TABLES")

for x in mycursor:
    print(x)
#mycursor.execute("SELECT * FROM scouts_1")
#myresult = mycursor.fetchall()
mycursor.execute("DESCRIBE scouts_1")
for x in mycursor:
    print(x[0])
managment_window()
# mydb.commit()

#print("Row inserted , ID", mycursor.lastrowid)
# for x in mycursor:
#    print(x)
