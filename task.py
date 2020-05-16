"""
Class for a task abstraction.
"""

class Task:
    """ This is a class representing task entity. """

    def __init__(self, name="New task", activity_periods=None):
        """
        Initialize task entity.

        The task entity is needed to account all activity's busy periods.

        :param name: name of the activity
        :param activity_periods: list of tuples (start_time, end_time)
        """
        self.name = name
        if activity_periods != None:
            self.activity_periods = activity_periods
        else:
            self.activity_periods = []

    def change_task_name(self, new_name):
        """ Assign a new name to the task """
        self.name = new_name

    def add_activity_period(self, start_time, end_time):
        """ Add start and end times of a new activity periods into the list."""
        self.activity_periods.append((start_time, end_time))
