#!/usr/bin/env python3
"""
Created on Sun May 17 00:39:50 2020

@author: embden
"""

from task import Task, task_id
from csv_data_organizer import CSVDataOrganizer
from datetime import timedelta, datetime


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
        self.existing_categories = dict()

    def add_new_task(self, task_name, task_category=None, activity_periods=None):
        """ Add the task to the list of possible tasks. """
        tmp_task = Task(task_name, task_category, activity_periods)
        # TODO: what should we do if there is a task with an equal name?
        # Generate exception NameExists?
        self.session_tasks[task_id(task_name, task_category)] = tmp_task
        self.write_changes_for_task(self.session_tasks[task_id(task_name, task_category)])

    def make_task_active(self, task_name, task_category):
        """ Add the task to the list of active tasks. """
        # TODO: Exception handling is required here
        self.active_tasks[task_id(task_name, task_category)] =\
            self.session_tasks[task_id(task_name, task_category)]
        self.session_tasks[task_id(task_name, task_category)].start_task()

    def make_task_stopped(self, task_name, task_category):
        """ Add the task to the list of stopped tasks. """
        # TODO: Exception handling is required here
        self.active_tasks.pop(task_id(task_name, task_category))
        self.session_tasks[task_id(task_name, task_category)].stop_task()
        self.task_db.write_tasks_data([self.session_tasks[task_id(task_name, task_category)]])

    def get_previous_tasks(self, period=7):
        """ Read tasks from the task database. """
        previous_tasks = self.task_db.read_previous_tasks(period)
        for task_to_add in previous_tasks:
            if task_to_add.category in self.existing_categories.keys():
                self.existing_categories[task_to_add.category] += 1
            else:
                self.existing_categories[task_to_add.category] = 1
            self.add_new_task(task_to_add.name, task_to_add.category,
                              task_to_add.activity_periods)
        return previous_tasks
    
    def get_tasks_and_duration(self, period=7, min_dur_bound=5):
        """ Get dicts of tasks and their durations. """
        tasks_and_durs = dict()
        finish_before = datetime.now() - timedelta(days=period)
        # A lot of unneeded loads and stores, can be optimized
        for tmp_task_id in self.session_tasks.keys():
            tasks_and_durs[tmp_task_id] = 0.0
            for period in self.session_tasks[tmp_task_id].activity_periods:
                if period[1] > finish_before:
                    tasks_and_durs[tmp_task_id] += (period[1]-period[0])/timedelta(hours=1)
        tasks_to_delete = []
        for tmp_task_id in tasks_and_durs.keys():
            if tasks_and_durs[tmp_task_id] < timedelta(minutes=min_dur_bound)/timedelta(hours=1):
                tasks_to_delete.append(tmp_task_id)
        for a in tasks_to_delete:
            del tasks_and_durs[a]
        return tasks_and_durs

    def get_existing_categories(self):
        """ Get known categories from history. """
        return list(self.existing_categories.keys())

    def write_changes_for_task(self, task_c):
        """ Write changes on disk and clean the cache. """
        self.task_db.write_tasks_data([task_c])
        task_c.new_activity_periods = []
