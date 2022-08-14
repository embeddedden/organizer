#!/usr/bin/env python3
"""
Created on Sun Jun  7 18:05:06 2020

@author: embden
"""

from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock


class Pomidorro(ProgressBar):
    """ Implement pomidorro timer. """
    
    def __init__(self, **kwargs):
        """ Initialize ProgressBar and Pomidorro. """
        super().__init__(**kwargs)
        
    def start(self):
        """ Start pomidorro timer from zero. """
        self.pomid_event = Clock.create_trigger(self.update, 
                                                timeout=60, interval=True)
        self.pomid_event()
    
    def stop(self):
        """ Stop pomidorro and set its value to zero"""
        self.value = 0
        self.pomid_event.cancel()
        
    def update(self, *args):
        """ Add a minute  to pomiddoro """
        if self.value+1 <= self.max:
            self.value += 1
        # else: show popup
