#!/usr/bin/env python3
"""
Created on Sun May 17 00:39:50 2020

@author: embden
"""

from task import Task

class TaskDispatcher:
    """ Implement inner logic of task management. """

    def __init__(self, session_tasks=None):
        """ Initialize Task Dispatcher."""

        if session_tasks is not None:
            self.session_tasks = session_tasks
        else:
            self.session_tasks = dict()
        self.active_tasks = dict()

    def add_new_task(self, task_name, activity_periods=None):
        """ Add the task to the list of possible tasks. """
        tmp_task = Task(task_name, activity_periods)
        #TODO: what should we do if there is a task with an equal name?
        # Generate exception NameExists?
        self.session_tasks[task_name] = tmp_task

    def make_task_active(self, task_name):
        """ Add the task to the list of active tasks. """
        #TODO: Exception handling is required here
        self.active_tasks[task_name] = self.session_tasks[task_name]
        self.session_tasks[task_name].start_task()

    def make_task_stopped(self, task_name):
        """ Add the task to the list of stopped tasks. """
        #TODO: Exception handling is required here
        self.active_tasks.pop(task_name)
        self.session_tasks[task_name].stop_task()
        