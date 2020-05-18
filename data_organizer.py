#!/usr/bin/env python3
"""
Created on Mon May 18 20:13:04 2020

@author: embden
"""

class DataOrganizer:
    """ Abstract class defining interface for CSV, DB managers. """
    
    def __init__():
        pass
    
    def read_previous_tasks(self, period):
        """ 
        Read task data from database.
        
        :param period: start and end dates of period of requested tasks.
        :returns: a list of Tasks.
        """
        pass
        
    def read_previous_tasks_names(self, period):
        """ 
        Read task data from database.
        
        :param period: start and end dates of period of requested tasks.
        :returns: a list of Task names for creating list of tasks.
        """
        pass
    
    def write_tasks_data(self, tasks_data):
        """
        Write tasks data into a database.
        
        :param tasks_data: a list of Task entities.
        """