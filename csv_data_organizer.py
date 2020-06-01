#!/usr/bin/env python3
"""
Created on Wed May 20 19:03:22 2020

@author: embden
"""

import csv
from datetime import datetime, timedelta
from data_organizer import DataOrganizer
from task import Task, task_id

class CSVDataOrganizer(DataOrganizer):
    """
    Read and write data to csv storage.

    Right now, there are the following fileds:
    category_name, task_name, start_time, finish_time
    """

    def __init__(self):
        """ Initialize CSV-based storage. """
        self.filename = "task_db.csv"

    def read_previous_tasks(self, period=None):
        """ Read data from the storage. """
        try:
            with open(self.filename, 'r') as csv_handler:
                csv_reader = csv.reader(csv_handler, delimiter='|')
                task_dict = dict()
                finish_before = datetime.now() - timedelta(days=period)
                for row in csv_reader:
                    task_category = row[0]
                    task_name = row[1]
                    task_activity = (datetime.fromisoformat(row[2]),
                                     datetime.fromisoformat(row[3]))
                    if task_activity[1] < finish_before:
                        continue
                    if task_id(task_name, task_category) not in task_dict:
                        task_dict[task_id(task_name, task_category)] = \
                        Task(task_name, task_category, [task_activity])
                    else:
                        task_dict[task_id(task_name, task_category)].\
                        activity_periods.append(task_activity)
                return list(task_dict.values())
        except FileNotFoundError:
            return []

    def write_tasks_data(self, tasks):
        """ Write data to CSV storage. """
        #TODO: what kind of error handling should be here
        with open(self.filename, 'a') as csv_handler:
            csv_writer = csv.writer(csv_handler, delimiter='|')
            for task_it in tasks:
                for activity_tuple in task_it.new_activity_periods:
                    csv_writer.writerow([task_it.category, task_it.name,
                                         activity_tuple[0], activity_tuple[1]])
