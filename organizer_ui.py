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
from kivy.core.window import Window

BUTTON_HEIGHT = 70

class TaskButton(Button):

    def __init__(self, **kwargs):

        super(TaskButton, self).__init__(**kwargs)
        self.register_event_type('on_relocate_event')

    def on_relocate_event(self, *args):

        pass

    def on_press(self):

        self.dispatch('on_relocate_event')

class VertBoxLayout(BoxLayout):

    def __init__(self, **kwargs):

        super(VertBoxLayout, self).__init__(**kwargs)
        self.empty_label = Label(size_hint=(None, None),
                                 text="Нет текущих задач",
                                 size=(Window.width, BUTTON_HEIGHT))
        super().add_widget(self.empty_label)

    def add_widget(self, *args):

        if self.children[0] == self.empty_label:
            super().remove_widget(self.empty_label)

        super().add_widget(*args)

    def remove_widget(self, *args):

        super().remove_widget(*args)
        if not self.children:
            super().add_widget(self.empty_label)


class TaskScrollView(ScrollView):

    def __init__(self, **kwargs):

        super(TaskScrollView, self).__init__(**kwargs)
        self.box_lt = VertBoxLayout(size_hint_y=None, orientation='vertical')
        self.box_lt.bind(minimum_height=self.box_lt.setter('height'))
        self.add_widget(self.box_lt)

    def add_descendant(self, obj):

        self.box_lt.add_widget(obj)

    def remove_descendant(self, obj):

        self.box_lt.remove_widget(obj)


class MainScreen(BoxLayout):

    def __init__(self, **kwargs):

        super(MainScreen, self).__init__(**kwargs)
        self.size_hint_x = None
        self.width = 300
        self.orientation = 'vertical'
        self.spacing = 8
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
        butt1 = TaskButton(text="Кодинг", size_hint=(None, None),
                           size=[Window.width, BUTTON_HEIGHT])
        butt1.bind(on_relocate_event=self.relocation_routine)
        self.task_buttons.add_descendant(butt1)
        butt2 = TaskButton(text="Работа", size_hint=(None, None),
                           size=[Window.width, BUTTON_HEIGHT])
        butt2.bind(on_relocate_event=self.relocation_routine)
        self.task_buttons.add_descendant(butt2)
        butt3 = TaskButton(text="Сериалыч", size_hint=(None, None),
                           size=[Window.width, BUTTON_HEIGHT])
        butt3.bind(on_relocate_event=self.relocation_routine)
        self.task_buttons.add_descendant(butt3)
        butt4 = TaskButton(text="Ютюб", size_hint=(None, None),
                           size=[Window.width, BUTTON_HEIGHT])
        butt4.bind(on_relocate_event=self.relocation_routine)
        self.task_buttons.add_descendant(butt4)

        add_task_button = Button(text="Добавить новую задачу",
                                 size_hint=(None, None),
                                 size=[Window.width, BUTTON_HEIGHT])
        self.add_widget(add_task_button)


    def relocation_routine(self, *args):

        if args[-1] in self.task_buttons.box_lt.children:
            self.task_buttons.remove_descendant(args[-1])
            self.current_tasks.add_descendant(args[-1])
        else:
            self.current_tasks.remove_descendant(args[-1])
            self.task_buttons.add_descendant(args[-1])
        print("Relocating")



class Organizer(App):

    def build(self):

        return MainScreen()

if __name__ == '__main__':
    Organizer().run()
