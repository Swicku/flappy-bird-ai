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
import time

Builder.load_file('bird.kv')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


def init():
    pass


class Bird(Widget):
    jump_force = 15
    mass = 1
    velocity = Vector(0, 0)
    max_gravity_force = 5
    max_jump_force = 7

    def clamp_force(self, a):
        return numpy.clip(a, -self.max_gravity_force, self.max_jump_force)

    def update_position(self):
        self.pos[1] += self.velocity[1]
        pass

    def apply_force(self, force):
        self.velocity[1] += force
        self.velocity[1] = float(self.clamp_force(self.velocity[1]))

    def jump(self):
        self.apply_force(self.jump_force)
        pass


class Wall(Widget):
    velocity = Vector(0, 0)
    pass


class Game(Widget):
    gravity_force = -0.2
    gap_size = 0
    bird = ObjectProperty(None)
    bottom_wall = ObjectProperty(None)
    top_wall = ObjectProperty(None)

    def init_game(self, gravity_force, gap_ratio):
        self.gap_size = self.height / gap_ratio
        self.gravity_force = gravity_force
        self.bird.center = self.center

    def manage_bird(self):
        bird_gravity_force = self.gravity_force * self.bird.mass
        if self.bird.pos[1] <= 0:
            bird_gravity_force = 0
        self.bird.apply_force(bird_gravity_force)
        self.bird.update_position()

        if self.bird.pos[1] >= self.height and self.bird.velocity[1] > 0:
            self.bird.velocity[1] = 0
        if self.bird.pos[1] <= 0 and self.bird.velocity[1] < 0:
            self.bird.velocity[1] = 0

    def manage_walls(self):
        is_first_time = True
        initial_velocity = -3

        if is_first_time:
            self.bottom_wall.velocity[0] = initial_velocity
            self.top_wall.velocity[0] = initial_velocity
            is_first_time = False

        self.bottom_wall.pos[0] += self.bottom_wall.velocity[0]
        self.top_wall.pos[0] += self.top_wall.velocity[0]

        if self.bottom_wall.pos[0] <= 0 and self.top_wall.pos[0] <= 0:
            self.calculate_walls(self.top_wall, self.bottom_wall)

    def calculate_walls(self, main_wall, other_wall):
        wall_speed = randint(-5, -3)

        main_wall.pos[0] = self.width
        main_wall_height = randint(int(self.height / 3), int(self.height / 1.5))
        main_wall.size = Vector(self.bird.width * 2, main_wall_height)

        other_wall_height = self.height - main_wall_height - self.gap_size
        other_wall.size = Vector(self.bird.width * 2, other_wall_height)
        other_wall.pos = Vector(self.width, self.height - other_wall.size[1])

        main_wall.velocity[0] = wall_speed
        other_wall.velocity[0] = wall_speed

    def update(self, dt):
        self.manage_bird()
        self.manage_walls()


class FlappyApp(App):
    parent = Game()
    gravity_force = -0.2
    gap_ratio = 10
    parent.init_game(gravity_force, gap_ratio)

    def build(self):
        jumpbtn = Button(text='jump')
        jumpbtn.bind(on_release=self.jump)
        self.parent.add_widget(jumpbtn)
        Clock.schedule_interval(self.parent.update, 1.0 / 60.0)
        return self.parent

    def jump(self, obj):
        self.parent.bird.jump()
        pass


# Running the whole thing
if __name__ == '__main__':
    FlappyApp().run()

# last_signal = [
#     self.bird.pos[1],  # birds y-axis position
#     self.bird.velocity[1],  # birds y-axis velocity
#     bottom_wall_x_pos - self.bird.pos[0],  # distance between bird and wall
#     gap_middle_y_pos - self.bird.pos[1],  # difference of heights between bird and gap
#     wall_speed
# ]


    # def manage_walls(self):
    #     is_first_time = True
    #     initial_velocity = -3
    #
    #     if is_first_time:
    #         self.bottom_wall.velocity[0] = initial_velocity
    #         self.top_wall.velocity[0] = initial_velocity
    #         is_first_time = False
    #
    #     self.bottom_wall.pos[0] += self.bottom_wall.velocity[0]
    #     self.top_wall.pos[0] += self.top_wall.velocity[0]
    #
    #     if self.bottom_wall.pos[0] <= 0 and self.top_wall.pos[0] <= 0:
    #         self.calculate_walls(self.top_wall, self.bottom_wall)
    #
    #     global bottom_wall_x_pos
    #
    #     global gap_middle_y_pos
    #
    #     bottom_wall_x_pos = self.bottom_wall.pos[0]
    #
    #     gap_pos = self.bottom_wall.size[1] + (self.height - self.bottom_wall.size[1] - self.top_wall.size[1]) / 2
    #
    #     gap_middle_y_pos = gap_pos