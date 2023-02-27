# Self Driving Car
import numpy
# Importing the libraries
import numpy as np
from random import random, randint
import matplotlib.pyplot as plt
import time

# Importing the Kivy packages
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.config import Config
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.core.window import Window

from Game import Game
from ai import Dqn

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class FlappyApp(App):
    time_interval = 0.000000005

    game = Game(
        gravity_force=-10
    )

    def build(self):
        jumpbtn = Button(text='jump')
        jumpbtn.bind(on_release=self.jump)
        self.game.add_widget(jumpbtn)
        Clock.schedule_interval(self.game.update, self.time_interval)
        return self.game

    def jump(self, obj):
        self.game.bird_jump()
        pass


# Running the whole thing
if __name__ == '__main__':
    FlappyApp().run()
