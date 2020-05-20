"""
Class for a task abstraction.
"""

from datetime import datetime

class Task:
    """ This is a class representing task entity. """

    def __init__(self, name="New task", category=None, activity_periods=None):
        """
        Initialize task entity.

        The task entity is needed to account all activity's busy periods.

        :param name: name of the activity
        :parem category: category of the activity
        :param activity_periods: list of tuples (start_time, end_time)
        """
        if category is not None:
            self.category = category
        else:
            self.category = "Empty"

        if name is not None:
            self.name = name
        else:
            self.name = "New task"
        self.state = 'Stopped' # or Active, or Paused
        self.current_start_time = None
        if activity_periods is not None:
            self.activity_periods = activity_periods
        else:
            self.activity_periods = []

    def change_task_name(self, new_name):
        """ Assign a new name to the task """
        self.name = new_name

    def add_activity_period(self, start_time, end_time):
        """ Add start and end times of a new activity periods into the list."""
        self.activity_periods.append((start_time, end_time))

    def start_task(self):
        """ Start countig time for the task. """
        self.current_start_time = datetime.now()
        self.state = 'Active'

    def stop_task(self):
        """ Stop counting time for the task. """
        self.activity_periods.append((self.current_start_time, datetime.now()))
        self.state = 'Stopped'
        print("Task is accomplished, duration:", self.activity_periods[0])

    def pause_task(self):
        """ Pause the counting time for the task. """
        self.stop_task()
        self.state('Stopped')

    def unpause_task(self):
        """ Unpause the paused task """
        self.start_task()
