# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 16:33:44 2024

@author: Jack Rawlinson

Creating a calendar window for use in another project
"""
import tkinter as tk
import datetime


class Calendar:

    def __init__(self, window):

        self.window = window
        # Get current month and year
        curr_time = datetime.datetime.now()

        self.curr_month = int(curr_time.strftime("%m"))

        self.year = int(curr_time.strftime("%Y"))

        self.weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        # Array with months and number of days in them
        self.months = [["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                        "Oct", "Nov", "Dec"], [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]]
        # check for leap year
        self.leap_year()

        tk.Button(self.window, text="<", command=self.previous_month).grid(row=0, column=0)
        tk.Button(self.window, text=">", command=self.next_month).grid(row=0, column=2)
        tk.Button(self.window, text="<", command=lambda: self.update_year(-1)).grid(row=0, column=4)
        tk.Button(self.window, text=">", command=lambda: self.update_year(1)).grid(row=0, column=6)

        self.create_calendar()

    def create_calendar(self):
        """
        Create the calander and set up window

        Returns
        -------
        None.

        """
        month_index = self.curr_month - 1
        # Use month and year to find what day the month started on
        first_of_month = datetime.datetime(self.year, self.curr_month, 1)
        fom_day = int(first_of_month.strftime("%w")) - 1

        # Array to store widgets
        self.dates = [None for i in range(35)]
        date = "  "
        # Month and year act as headers to calendar
        tk.Label(self.window, text=self.months[0][month_index]).grid(row=0, column=1)
        tk.Label(self.window, text=self.year).grid(row=0, column=5)

        # Add weekdays
        for column_itr in range(7):
            tk.Label(self.window, text=self.weekdays[column_itr]).grid(row=1, column=column_itr)

        # Add dates for current month
        for row_itr in range(2, 7):
            for column_itr in range(7):

                index = (row_itr - 2)*7 + column_itr
                # Start month on correct day
                if index == fom_day:
                    date = 1
                #print(f'Loop {index}, column_itr = {column_itr}, date = {date}, fom_day = {fom_day}')
                self.dates[index] = tk.Label(self.window, text=date)
                self.dates[index].grid(row=row_itr, column=column_itr)
                self.dates[index].bind("<Button-1>", self.date_picked)

                if date == self.months[1][month_index] or date == "  " or (column_itr < fom_day and row_itr == 2):
                    date = "  "
                else:
                    date += 1

    def previous_month(self):
        """
        Update the month being viewed

        Returns
        -------
        None.

        """
        self.curr_month -= 1
        if self.curr_month == 0:
            self.curr_month = 12
        self.create_calendar()

    def next_month(self):
        """
        Update the month being viewed

        Returns
        -------
        None.

        """
        self.curr_month += 1
        if self.curr_month == 12:
            self.curr_month = 1
        self.create_calendar()

    def update_year(self, increment):
        """
        Update the year being viewed

        Returns
        -------
        None.

        """
        self.year += increment
        self.leap_year()
        self.create_calendar()

    def leap_year(self):
        """
        Check if its a leap year and update Feb

        Returns
        -------
        None.

        """
        self.months[1][1] = 28
        if self.year % 4 == 0:
            self.months[1][1] = 29

    def date_picked(self, event):
        """
        Highlights last pressed date and opens text widget to allow for text

        Parameters
        ----------
        event : Button-1 press event 

        Returns
        -------
        None.

        """
        # Remove any already blue labels
        for i in range(35):
            self.dates[i].config(bg="#f0f0f0")
        # Highlight label
        widget = event.widget
        widget.config(bg="light blue")
        # Create text box
        tk.Text(self.window, height=10, width=15).grid(row=0, column=7, rowspan=9, columnspan=1)
