#!/usr/bin/env python3
"""
Created on Sun May 17 00:39:50 2020

@author: embden
"""

from task import Task, task_id
from csv_data_organizer import CSVDataOrganizer

class TaskDispatcher:
    """ Implement inner logic of task management. """

    def __init__(self, session_tasks=None):
        """ Initialize Task Dispatcher."""

        if session_tasks is not None:
            self.session_tasks = session_tasks
        else:
            self.session_tasks = dict()
        self.active_tasks = dict()
        self.task_db = CSVDataOrganizer()

    def add_new_task(self, task_name, task_category="Empty", activity_periods=None):
        """ Add the task to the list of possible tasks. """
        tmp_task = Task(task_name, task_category, activity_periods)
        #TODO: what should we do if there is a task with an equal name?
        # Generate exception NameExists?
        self.session_tasks[task_id(task_name, task_category)] = tmp_task
        self.write_changes_for_task(self.session_tasks[task_id(task_name, task_category)])

    def make_task_active(self, task_name, task_category):
        """ Add the task to the list of active tasks. """
        #TODO: Exception handling is required here
        self.active_tasks[task_id(task_name, task_category)] =\
        self.session_tasks[task_id(task_name, task_category)]
        self.session_tasks[task_id(task_name, task_category)].start_task()

    def make_task_stopped(self, task_name, task_category):
        """ Add the task to the list of stopped tasks. """
        #TODO: Exception handling is required here
        self.active_tasks.pop(task_id(task_name, task_category))
        self.session_tasks[task_id(task_name, task_category)].stop_task()
        self.task_db.write_tasks_data([self.session_tasks[task_id(task_name, task_category)]])

    def get_previous_tasks(self, period=None):
        """ Read tasks from the task database. """
        previous_tasks = self.task_db.read_previous_tasks()
        for task_to_add in previous_tasks:
            self.add_new_task(task_to_add.name, task_to_add.category,
                              task_to_add.activity_periods)
        return previous_tasks

    def write_changes_for_task(self, task_c):
        """ Write changes on disk and clean the cache. """
        self.task_db.write_tasks_data([task_c])
        task_c.new_activity_periods = []
