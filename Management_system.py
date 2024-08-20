# -*- coding: utf-8 -*-
"""
Created on Mon Aug 05 16:40 2024

Scout Management System

@author: Jack Rawlinson
"""
import tkinter as tk
import mysql.connector
import Calendar_widget


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
        self.create_entry.grid(row=0, column=0, rowspan=2, columnspan=3)

        self.show_entries = tk.Button(self.window, text="Show Entries",
                                      command=self.show_table_entries)
        self.show_entries.grid(row=0, column=3, rowspan=2, columnspan=3)

        tk.Button(self.window, text="Edit columns", command=self.edit_table).grid(
            row=0, column=6, columnspan=3)

        # Add a calendar to the window
        frame = tk.Frame(self.window)
        frame.grid(row=20, column=8, rowspan=42)
        Calendar_widget.Calendar(window=frame)

        # Find amount of columns
        self.mycursor.execute(
            "SELECT count(*) AS anyName FROM information_schema.columns WHERE table_name = 'scouts_1';")
        length = self.mycursor.fetchall()[-1][-1]
        # Initilaise 2D array to store display widgets
        self.display_grid = [[None for i in range(length)]]

        # Create window
        self.window.mainloop()

    def reset_display_grid(self):
        """


        Returns
        -------
        None.

        """
        widget = tk.widget()
        for i in range(len(self.display_grid)):
            for j in range(len(self.display_grid[i])):
                if isinstance(self.display_grid[i][j], widget):
                    self.display_grid[i][j].destroy()

    def create_entry(self):
        """
        Allows user to added a new entry to current table within the database 

        Returns
        -------
        None.

        """
        # Find amount of columns
        self.mycursor.execute(
            "SELECT count(*) AS anyName FROM information_schema.columns WHERE table_name = 'scouts_1';")
        length = self.mycursor.fetchall()[-1][-1]

        self.display_grid = [[0 for column in range(length + 1)] for row in range(2)]

        # Retriving the column titles for entry
        self.mycursor.execute("DESCRIBE scouts_1")

        # Define positions of the widgets
        row_position = 3
        column_position = 1
        iterator = 0

        # Iterate over all columns in database table
        for col in self.mycursor:

            # Title to show user what each entry box corresponds to
            self.display_grid[0][iterator] = tk.Label(text=col[0])
            self.display_grid[0][iterator].grid(
                row=row_position, column=column_position, columnspan=3)

            self.display_grid[1][iterator] = tk.Entry(self.window, justify="center")

            self.display_grid[1][iterator].grid(
                row=row_position+1, column=column_position, columnspan=3)
            column_position += 3
            iterator += 1

        self.display_grid[1][iterator] = tk.Button(
            self.window, text="Add entry", command=self.add_entry)
        self.display_grid[1][iterator].grid(row=5, column=column_position)
        # self.window.update()
        print("In create entry")

    def add_entry(self):
        """
        Adds an entry to the table in sql datebase

        Returns
        -------
        None.

        """
        print("In add entry")

        # Temp array to store data that will be added to the data base
        desired_entry = [0 for i in range(len(self.display_grid[0]) - 1)]

        # SQL command to add the data
        sql_command = "INSERT INTO scouts_1 (id, name, Guardian1, Guardian1_contact, Guardian2) VALUES (%s, %s,%s, %s,%s)"

        # Check that entry box has values in it
        if self.display_grid[1][0] != None:

            for i in range(len(self.display_grid[0]) - 1):
                print(f'Loop number = {i}')

                desired_entry[i] = self.display_grid[1][i].get()

                # Remove entry options once data has been stored
                self.display_grid[0][i].destroy()
                self.display_grid[1][i].destroy()
            #val = (('John', 'mum', 'mum_contact', 'dad', 'dad_contact'))
            print(f'Leaving for loop values = {desired_entry}')
            self.display_grid[1][-1].destroy()

            # Input data into table
            self.mycursor.execute(sql_command, desired_entry)
            print("Data inserted")

        # Commit changes to database
        self.mydb.commit()

    def show_table_entries(self):
        """
        Shows current contents of the table

        Returns
        -------
        None.

        """
        print("Entering show entries")
        # Fetching data from required table in database
        self.mycursor.execute("SELECT * FROM scouts_1")
        result = self.mycursor.fetchall()
        # Find amount of columns
        self.mycursor.execute(
            "SELECT count(*) AS anyName FROM information_schema.columns WHERE table_name = 'scouts_1';")
        length = self.mycursor.fetchall()[-1][-1]

        # Retriving the column titles for entry
        #self.mycursor.execute("DESCRIBE scouts_1")
        print(f'len(length) = {length}')
        print("Creating display grid")
        self.display_grid = [[0 for column in range(length + 1)] for row in range(len(result)+1)]
        print(self.display_grid)

        # Define positions of the widgets
        row_position = 3
        column_position = 1
        iterator = 0

        # Fetching data from required table in database
        self.mycursor.execute("SELECT * FROM scouts_1")
        result = self.mycursor.fetchall()
        # Retriving the column titles for entry
        self.mycursor.execute("DESCRIBE scouts_1")
        print("Entering header loop")
        # Iterate over all columns in database table
        for col in self.mycursor:
            print("Creating column headers")
            # Title to show user what each entry box corresponds to
            self.display_grid[0][iterator] = tk.Label(self.window, text=col[0])
            self.display_grid[0][iterator].grid(
                row=row_position, column=column_position, columnspan=3)
            print(result[0][iterator])
            column_position += 3
            iterator += 1
        row_position += 1

        print("Entering for loop")

        for row in result:

            # Reset positions ready for a new row of data
            column_position = 1
            iterator = 0
            print("in row loop")

            # Execute command again to allow for iteration
            #self.mycursor.execute("DESCRIBE scouts_1")

            #temp_array = [0 for i in self.mycursor]

            # Execute command again to allow for iteration
            self.mycursor.execute("DESCRIBE scouts_1")

            for col in self.mycursor:

                print(col[0])
                print("Showing Column items")
                print(row[iterator])
                print(row[1])
                print(f'row index = {row_position-3}')
                print(self.display_grid)
                # Create label to show data
                self.display_grid[row_position-3][iterator] = 10
                self.display_grid[row_position -
                                  3][iterator] = tk.Label(self.window, text=row[iterator])
                self.display_grid[row_position -
                                  3][iterator].grid(row=row_position, column=column_position, columnspan=3)
                column_position += 3
                iterator += 1

            #self.display_grid[row_position-3] = temp_array

            # Finish each row with a delete button in case data needs to be removed
            self.display_grid[row_position-3][iterator] = tk.Button(self.window, text="Delete")
            self.display_grid[row_position -
                              3][iterator].grid(row=row_position, column=column_position)
            self.display_grid[row_position-3][iterator].bind("<Button-1>", self.delete_entry)

            # Update row
            row_position += 1
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
        print("Deleteing an entry")
        # Find where the pressed button is and use this to obtain the id of the data
        grid_position = event.widget.grid_info()
        button_row = grid_position["row"]
        entry_id = int(button_row - 3)

        print(f'len(self.display_grid) = {len(self.display_grid)}')
        print(f'len(self.display_grid[0]) = {len(self.display_grid[0])}')
        print(self.display_grid[0])

        for i in range(len(self.display_grid[0])):
            print(f'i = {i}, Type = {type(int(i))}')
            print(f'entry_id = {entry_id}, Type = {type(entry_id)}')
            print(f'self.display_grid[entry_id][i] = {self.display_grid[entry_id][i]}')
            self.display_grid[entry_id][i].destroy()

        print(entry_id)
        # Delete data row from SQL table
        self.mycursor.execute(f'DELETE FROM scouts_1 WHERE id = "{entry_id}" ')
        # Commit change to database
        self.mydb.commit()

        print("deleteing grid")
        # self.delete_display_grid()
        print("Recreating grid")
        # self.show_table_entries()

    def edit_table(self):

        self.mycursor.execute("DESCRIBE scouts_1")
        # Define positions of the widgets
        row_position = 3
        column_position = 1

        # Iterate over all columns in database table
        for col in self.mycursor:

            # Title to show user what each entry box corresponds to
            tk.Label(self.window, text=col[0]).grid(
                row=row_position, column=column_position, columnspan=3)
            tk.Button(self.window, text="x").grid(row=row_position, column=column_position+3)
            column_position += 4
        add_column = tk.Button(self.window, text="\u002b",
                               command=lambda: self.add_column(column_position))
        add_column.grid(row=row_position, column=column_position)

    def add_column(self, current_column):

        self.new_column = tk.Entry(self.window)
        self.new_column.grid(row=3, column=(current_column+2))
        self.new_column.bind("<Return>", self.confirm_column(current_column))

    def confirm_column(self, col):
        tk.Label(self.window, text=self.new_column.get()).grid(row=3, column=col)
        print("Entered confirm column")
        print(f'Column seen is named: {self.new_column.get()}')


if __name__ == "__main__":
    managment_window()
