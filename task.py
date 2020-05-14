"""
Class for a task abstraction.
"""
from datetime import timedelta, datetime

class Task:
    """ This is a class representing task entity. """

    def __init__(self):
        self.name = "Empty task"
        self.start_time = datetime.now()
        self.delta = timedelta(hours=1)
        self.end_time = datetime.now() + self.delta

    def change_start_time(self, new_start_time):
        """ Change start time of the task """
        self.start_time = new_start_time

    def change_end_time(self, new_end_time):
        """ Change end time of the task """
        self.end_time = new_end_time

    def change_task_name(self, new_name):
        """ Assign a new name to the task """
        self.name = new_name
