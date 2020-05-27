#!/usr/bin/env python3
"""
Created on Wed May 27 17:36:55 2020

@author: embden
"""
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
from textwrap import wrap
import numpy as np

def format_label(pct, allvals):
    absolute = int(round(pct/100.*np.sum(allvals), 2))
    hours = absolute
    mins = int((round(pct/100.*np.sum(allvals), 2) - float(hours))*60)
    return "{:.2f}% ({:d}:{:d})".format(pct, hours, mins)

class MatPlotter(BoxLayout):
    """
    Plots matplotlib graphs based on provided dict data.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        plt.figure()
        self.fir1, self.ax1 = plt.subplots()
        self.graph = FigureCanvasKivyAgg(plt.gcf())
        self.add_widget(self.graph)
        
    def update_graph(self, graph_data):
        """
        Draws graph based on graph_data dict.
        """
        labels_for_pie = []
        values_for_pie = []
        sorted_view = sorted(graph_data.items())
        for i in sorted_view:
            labels_for_pie.append('\n'.join(wrap(i[0], 50)))
            values_for_pie.append(i[1])
        self.ax1.pie(values_for_pie, 
                     autopct=lambda pct:format_label(pct, values_for_pie))
        plt.legend(labels_for_pie, bbox_to_anchor=(0, 0), loc='upper left')
