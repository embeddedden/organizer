#!/usr/bin/env python3
"""
Created on Mon May 18 20:13:04 2020

@author: embden
"""

from abc import ABC, abstractmethod

class DataOrganizer(ABC):
    """ Abstract class defining interface for CSV, DB managers. """

    @abstractmethod
    def read_previous_tasks(self, period):
        """
        Read task data from database.

        :param period: start and end dates of period of requested tasks.
        :returns: a list of Tasks.
        """

    @abstractmethod
    def write_tasks_data(self, tasks):
        """
        Write tasks data into a database.

        :param tasks: a list of Task entities.
        """
