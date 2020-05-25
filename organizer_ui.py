#!/usr/bin/env python3
"""
Created on Fri May  1 20:59:21 2020

@author: embden
"""
from kivy.config import Config
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '640')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
from task_dispatcher import TaskDispatcher

# Regulate button height through this parameter.
BUTTON_HEIGHT = 70

class TaskButton(Button):
    """
    Class representing a button for a task expanding standard kivy button.

    The distinctive feature of the class is its capability to be in two states:
    active or waiting. In active state a button shold look like a push button.
    Thus, when a user starts to work on a task he pushes the button, and when
    finishes - releases it.
    """

    def __init__(self, **kwargs):
        """ Expand Button kivy class. """
        super(TaskButton, self).__init__(**kwargs)
        self.register_event_type('on_relocate_event')
        self.category = 'Empty'
        self.activity_state = 'Waiting' # or 'Active', or 'Removed'
        self.name = self.text
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.time_in_seconds = 0
        self.c_event = Clock.create_trigger(self.update_clock, timeout=1,
                                            interval=True)

    def on_relocate_event(self, *args):
        """ Default handler for on_relocate_event. """
        pass

    def on_press(self):
        """ Override default on_press handler. """
        self.dispatch('on_relocate_event')
        #TODO: we should remove background_normal because it is mixed with
        #background_color
        if self.activity_state == 'Waiting':
            self.c_event()
            self.activity_state = 'Active'
            self.background_color = (0, 0.9, 0, 1)
            self.text = f'{self.name} ({self.hours:02}:{self.minutes:02}:{self.seconds:02})'
        else:
            self.activity_state = 'Waiting'
            self.c_event.cancel()
            self.background_color = (1, 1, 1, 1)

    def update_clock(self, *args):
        """ Update time for active task. """
        self.time_in_seconds += 1
        self.seconds = self.time_in_seconds % 60
        self.minutes = self.time_in_seconds // 60 % 60
        self.hours = self.time_in_seconds // 60 // 60 % 24
        self.text = f'{self.name} ({self.hours:02}:{self.minutes:02}:{self.seconds:02})'

class VertBoxLayout(BoxLayout):
    """
    A box layout that can receive and release TaskButtons.

    The class expands the default BoxLayout kivy widget. It adds a placeholder
    label for empty list.
    """

    def __init__(self, **kwargs):
        """ Initialize class by placing a placeholder Label. """
        super(VertBoxLayout, self).__init__(**kwargs)
        self.empty_label = Label(size_hint=(None, None),
                                 text="Нет текущих задач",
                                 size=(Window.width, BUTTON_HEIGHT))
        super().add_widget(self.empty_label)

    def add_widget(self, *args):
        """ Override BoxLayou.addWidget(). """
        if self.children[0] == self.empty_label:
            super().remove_widget(self.empty_label)

        super().add_widget(*args)

    def remove_widget(self, *args):
        """ Override BoxLayou.removeWidget(). """
        super().remove_widget(*args)
        if not self.children:
            super().add_widget(self.empty_label)

class TaskScrollView(ScrollView):
    """
    ScrollView that is able to receive and remove TaskButtons.

    Class consists of VertBoxLayout widget and is able to receive/send
    TaskButtons from/to its VertBoxLayout child. Class exapnd default Kive
    ScrollView class.
    """

    def __init__(self, **kwargs):
        """ Create a child VertBoxLayout widget and initialize class. """
        super(TaskScrollView, self).__init__(**kwargs)
        self.box_lt = VertBoxLayout(size_hint_y=None, orientation='vertical')
        self.box_lt.bind(minimum_height=self.box_lt.setter('height'))
        self.add_widget(self.box_lt)

    def add_descendant(self, obj):
        """ Add widget obj to the child box layout. """
        self.box_lt.add_widget(obj)

    def remove_descendant(self, obj):
        """ Remove widget obj from the child box layout. """
        self.box_lt.remove_widget(obj)

class MainScreen(BoxLayout):
    """
    Class for managing UI of the organizer application.

    It creates all the descendant widgets and place them in the BoxLayout. It
    also manages all the interaction between descendants, e.g. passing a
    TaskButton from one TaskScrollView->VertBoxLayout to the other.
    """

    def __init__(self, **kwargs):
        """ Initialize the main window and place all the elements."""
        super(MainScreen, self).__init__(**kwargs)
        self.size_hint_x = None
        self.width = 300
        self.orientation = 'vertical'
        self.spacing = 8
        self.task_dispatcher = TaskDispatcher()
        self.previous_tasks = self.task_dispatcher.get_previous_tasks()
        menu_box = BoxLayout(size_hint=(None, None), orientation='horizontal')
        menu_button = Button(text="Меню", size_hint=(None, None),
                             size=[Window.width, BUTTON_HEIGHT])
        menu_box.add_widget(menu_button)
        menu_box.bind(minimum_height=menu_box.setter('height'))
        menu_box.size_hint_max_y = menu_button.height+5
        self.add_widget(menu_box)


        taskbox_label = Label(size_hint=(None, None), text="Текущие задачи:")
        taskbox_label.bind(texture_size=taskbox_label.setter('size'))
        self.add_widget(taskbox_label)

        self.current_tasks = TaskScrollView(size_hint=(None, 1),
                                            width=Window.width)
        self.add_widget(self.current_tasks)

        new_taskbox_label = Label(size_hint=(None, None), text="Все задачи:")
        new_taskbox_label.bind(texture_size=new_taskbox_label.setter('size'))
        self.add_widget(new_taskbox_label)

        self.task_buttons = TaskScrollView(size_hint=(None, 1),
                                           width=Window.width)
        self.add_widget(self.task_buttons)
        self.task_buttons.bind(on_relocate_descendant=self.relocation_routine)
        for task_to_insert in self.previous_tasks:
            task_button = TaskButton(text=task_to_insert.name,
                                     size_hint=(None, None),
                                     size=[Window.width, BUTTON_HEIGHT])
            task_button.category = task_to_insert.category
            task_button.bind(on_relocate_event=self.relocation_routine)
            self.task_buttons.add_descendant(task_button)

        add_task_button = Button(text="Добавить новую задачу",
                                 size_hint=(None, None),
                                 size=[Window.width, BUTTON_HEIGHT])
        add_task_button.bind(on_press=self.create_new_task_popup)
        self.add_widget(add_task_button)

    def create_new_task_popup(self, *args):
        """ Create a popup for a new task. """
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.spacing = 5
        popup_layout.bind(minimum_height=popup_layout.setter('height'))
        create_btn = Button(text='Создать задачу',
                            size_hint_y=None,
                            height=BUTTON_HEIGHT)
        self.create_edit = TextInput(font_size=18, halign='center',
                                     hint_text='Введите название задачи',
                                     size_hint_y=None,
                                     height=BUTTON_HEIGHT,
                                     multiline=False)
        self.create_edit.bind(on_text_validate=self.create_task)
        popup_layout.add_widget(self.create_edit)
        popup_layout.add_widget(create_btn)
        self.popup = Popup(title='Создай новую задачу', content=popup_layout,
                           size_hint=(1, None),
                           height=create_btn.height+self.create_edit.height+100)
        create_btn.bind(on_release=self.create_task)
        self.popup.open()

    def create_task(self, *args):
        """ Add a task to session tasks. """
        #TODO: add exception handling
        self.task_dispatcher.add_new_task(self.create_edit.text)
        tmp_butt = TaskButton(text=self.create_edit.text,
                              size_hint=(None, None),
                              size=[Window.width, BUTTON_HEIGHT])
        tmp_butt.category = 'Empty'
        tmp_butt.bind(on_relocate_event=self.relocation_routine)
        self.task_buttons.add_descendant(tmp_butt)
        self.popup.dismiss()

    def relocation_routine(self, *args):
        """ Relocate a TaskButton from one layout to the other. """
        if args[-1] in self.task_buttons.box_lt.children:
            self.task_dispatcher.make_task_active(args[-1].name, args[-1].category)
            self.task_buttons.remove_descendant(args[-1])
            self.current_tasks.add_descendant(args[-1])
        else:
            self.task_dispatcher.make_task_stopped(args[-1].name, args[-1].category)
            self.current_tasks.remove_descendant(args[-1])
            self.task_buttons.add_descendant(args[-1])

class Organizer(App):
    """ Class representing the Application. """

    def build(self):
        """ Routine for creating the Window. """
        return MainScreen()

if __name__ == '__main__':
    Organizer().run()
