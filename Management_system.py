# -*- coding: utf-8 -*-
"""
Created on Mon Aug 05 16:40 2024

Scout Management System

@author: Jack Rawlinson
"""
import tkinter as tk
import mysql.connector
import numpy as np


class managment_window:
    def __init__(self):

        # Acessing database
        self.mydb = mysql.connector.connect(host="localhost", user="root",
                                            password="1stW0TH", database="scout_database")
        # initilize cursor
        self.mycursor = self.mydb.cursor()

        # Set up window
        self.window = tk.Tk()
        self.window.title("Scout Management")
        self.window.config(bg="#a000e4")

        # Initilize widgets on the window
        self.create_entry = tk.Button(
            self.window, text="Create New Entry", command=self.create_entry)
        self.create_entry.grid(row=1, column=1, rowspan=2, columnspan=3)

        self.show_entries = tk.Button(self.window, text="Show Entries", command=self.show_entries)
        self.show_entries.grid(row=1, column=4, rowspan=2, columnspan=3)

        # Create window
        self.window.mainloop()

    def create_entry(self):
        """
        Allows user to added a new entry to current table within the database 

        Returns
        -------
        None.

        """

        self.mycursor.execute(
            "SELECT count(*) AS anyName FROM information_schema.columns WHERE table_name = 'scouts_1';")
        length = self.mycursor.fetchall()[-1][-1]

        self.entry_data = [None for i in range(length)]

        # Retriving the column titles for entry
        self.mycursor.execute("DESCRIBE scouts_1")

        # Define positions of the widgets
        row_position = 3
        column_position = 1
        iterator = 0

        # Iterate over all columns in database table
        for col in self.mycursor:

            # Title to show user what each entry box corresponds to
            tk.Label(text=col[0]).grid(row=row_position, column=column_position, columnspan=3)
            self.entry_data[iterator] = tk.Entry(self.window, justify="center")

            self.entry_data[iterator].grid(row=row_position+1, column=column_position, columnspan=3)
            column_position += 3
            iterator += 1

        tk.Button(self.window, text="Add entry", command=self.add_entry).grid(
            row=5, column=column_position)
        # self.window.update()
        print("In create entry")

    def add_entry(self):
        print("In add entry")

        # Temp array to store data that will be added to the data base
        desired_entry = [0 for i in range(len(self.entry_data))]

        # SQL command to add the data
        sql_command = "INSERT INTO scouts_1 (id, name, Guardian1, Guardian1_contact, Guardian2) VALUES (%s, %s,%s, %s,%s)"

        # Check that entry box has values in it
        if self.entry_data[0] != None:

            for i in range(len(self.entry_data)):
                print(f'Loop number = {i}')
                print(f'self.entry_data = {self.entry_data}')
                print(f'entry = {self.entry_data[i].get()}')

                desired_entry[i] = self.entry_data[i].get()

                # Remove entry options once data has been stored
                self.entry_data[i].grid_remove()
            #val = (('John', 'mum', 'mum_contact', 'dad', 'dad_contact'))
            print(f'Leaving for loop values = {desired_entry}')

            # Input data into table
            self.mycursor.execute(sql_command, desired_entry)
            print("Data inserted")

        # Commit changes to database
        self.mydb.commit()

    def show_entries(self):
        """
        Shows current contents of the table

        Returns
        -------
        None.

        """
        # Fetching data from required table in database
        self.mycursor.execute("SELECT * FROM scouts_1")
        result = self.mycursor.fetchall()

        # Retriving the column titles for entry
        self.mycursor.execute("DESCRIBE scouts_1")

        # Define positions of the widgets
        row_position = 3
        column_position = 1
        iterator = 0

        # Iterate over all columns in database table
        for col in self.mycursor:

            # Title to show user what each entry box corresponds to
            tk.Label(self.window, text=col[0]).grid(
                row=row_position, column=column_position, columnspan=3)
            column_position += 3

        print("Entering for loop")
        column_position = 1
        for row in result:

            # Reset positions ready for a new row of data
            column_position = 1
            iterator = 0
            # Update row
            row_position += 1
            print("in row loop")

            # Execute command again to allow for iteration
            self.mycursor.execute("DESCRIBE scouts_1")
            for col in self.mycursor:

                print(col[0])
                print("Entered for loop")
                print(row[iterator])
                # Create label to show data
                tk.Label(self.window, text=row[iterator]).grid(
                    row=row_position, column=column_position, columnspan=3)
                column_position += 3
                iterator += 1

            # Finish each row with a delete button in case data needs to be removed
            delete_button = tk.Button(self.window, text="Delete")
            delete_button.grid(row=row_position, column=column_position)
            delete_button.bind("<Button-1>", self.delete_entry)
            print("Leaving row for loop")
        print("In show entries")

    def delete_entry(self, event):
        """
        Allows user to delete a data entry using a button

        Parameters
        ----------
        event : Button-1 event
          left mouse press event on the delete button 

        Returns
        -------
        None.

        """
        # Find where the pressed button is and use this to obtain the id of the data
        grid_position = event.widget.grid_info()
        button_row = grid_position["row"]
        entry_id = int(button_row - 3)

        print(entry_id)
        # Delete data row from SQL table
        self.mycursor.execute(f'DELETE FROM scouts_1 WHERE id = "{entry_id}" ')
        # Commit change to database
        self.mydb.commit()


"""
Experimenting with MySQL and gaining understanding of its functionality 
"""
# mydb = mysql.connector.connect(host="localhost", user="root",
#                               password="[D1x1e2021&D@isy2022]", database="scout_database")

#mycursor = mydb.cursor()

# mycursor.execute(
#    "ALTER TABLE scouts ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
#sql = "INSERT INTO scouts_1 (name, Guardian1, Guardian1_contact, Guardian2) VALUES (%s, %s,%s, %s,%s)"
#val = (('John', 'mum', 'mum_contact', 'dad', 'dad_contact'))
#mycursor.execute(sql, val)
#mycursor.execute("SHOW TABLES")

# for x in mycursor:
#    print(x)
#mycursor.execute("SELECT * FROM scouts_1")
#myresult = mycursor.fetchall()
#mycursor.execute("DESCRIBE scouts_1")
# for x in mycursor:
#    print(x[0])
managment_window()
# mydb.commit()

#print("Row inserted , ID", mycursor.lastrowid)
# for x in mycursor:
#    print(x)
