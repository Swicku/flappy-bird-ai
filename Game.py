import random
import time

from physics.Bird import Bird
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from physics.BottomWall import BottomWall
from physics.TopWall import TopWall
from ai import Dqn

# AI stuff
brain = Dqn(7, 2, 3)
last_reward = 0
# don't jump / jump
action2action = [0, 1]


def get_current_epoch_time():
    return int(time.time())


class Game(Widget):
    background = None
    bird = None
    gravity_force = None
    bird_size = (50, 50)
    initial_bird_pos = (Window.width / 3, Window.height / 2)
    initial_wall_height = Window.height / 4
    initial_top_wall_size = None
    initial_bottom_wall_size = None
    initial_top_wall_pos = None
    initial_bottom_wall_pos = None
    wall_width = None
    top_wall = None
    bottom_wall = None
    gap_size = Window.height / 2.2
    pipe_middle = None
    start_time = None

    def __init__(self, gravity_force):
        super().__init__()
        self.gravity_force = gravity_force
        with self.canvas:
            self.background = Rectangle(size=(Window.width, Window.height), source='./images/background.png')
            self.bird = Bird(Rectangle(pos=self.initial_bird_pos, size=self.bird_size, source='./images/bird.png'),
                             self.initial_bird_pos, self.bird_size)
            self.wall_width = self.bird.widget.size[0] * 2

            self.initial_bottom_wall_pos = (Window.width + self.wall_width, 0)
            self.initial_top_wall_pos = (Window.width + self.wall_width, Window.height - self.initial_wall_height)

            self.initial_top_wall_size = (self.wall_width, self.initial_wall_height)
            self.initial_bottom_wall_size = (self.wall_width, self.initial_wall_height)

            self.bottom_wall = BottomWall(
                Rectangle(pos=self.initial_bottom_wall_pos, size=self.initial_bottom_wall_size,
                          source='./images/wall.png'), self.initial_bottom_wall_pos, self.initial_bottom_wall_size)

            self.top_wall = TopWall(
                Rectangle(pos=self.initial_top_wall_pos, size=self.initial_top_wall_size,
                          source='./images/wall.png'), self.initial_top_wall_pos, self.initial_top_wall_size)
            self.start_time = get_current_epoch_time()

            # self.pipe_middle = Rectangle(pos=(0, Window.height / 2), size=(Window.width, 150),
            #                              source='./images/wall.png')

    def update(self, dt):

        global brain
        global last_reward
        # 0 - current bird height
        # 1 - wall width
        # 2 - x coordinate of bottom-left corner of bottom wall
        # 3 - current bottom wall height
        # 4 - x coordinate of bottom-left corner of top wall
        # 5 - current top wall height
        # 6 - wall speed

        last_signal = [
            self.bird.widget.pos[1],
            self.wall_width,
            self.bottom_wall.widget.pos[0],
            self.bottom_wall.widget.size[1],
            self.top_wall.widget.pos[0],
            self.top_wall.widget.size[1],
            self.bottom_wall.horizontal_velocity
        ]
        action = brain.update(last_reward, last_signal)
        jump = action2action[action]

        # print(jump)

        if jump == 1:
            self.bird.jump()

        pipe_center = self.bottom_wall.widget.size[1] + self.gap_size / 2

        if self.bird.widget.pos[1] > pipe_center + 70 or self.bird.widget.pos[1] < pipe_center - 70:
            if last_reward == 2:
                last_reward = -1
        else:
            last_reward = 2

        if self.bird.widget.pos[1] < 0:
            last_reward = -5
            self.reset_game()
        if self.bird.is_colliding_with(self.top_wall.widget.pos, self.top_wall.widget.size) \
                or self.bird.is_colliding_with(self.bottom_wall.widget.pos, self.bottom_wall.widget.size):
            last_reward = -2
            self.reset_game()
        if self.bottom_wall.widget.pos[0] + self.wall_width < 0:
            self.respawn_walls()

        print(last_reward)

        self.manage_bird(dt)
        self.manage_walls(dt)

    def bird_jump(self):
        self.bird.jump()

    def manage_bird(self, dt):
        self.bird.add_vertical_velocity(self.gravity_force)
        self.bird.transition(dt)
        if self.bird.widget.pos[1] > Window.height:
            self.bird.widget.pos = (self.bird.widget.pos[0], Window.height)
            self.bird.vertical_velocity = 0

    def manage_walls(self, dt):
        self.bottom_wall.transition(dt)
        self.top_wall.transition(dt)

    def reset_game(self):
        self.bird.reset()
        self.reset_walls()
        self.start_time = get_current_epoch_time()

    def respawn_walls(self):
        wall_speed = -random.randint(200, 300)
        self.bottom_wall.horizontal_velocity = wall_speed
        self.top_wall.horizontal_velocity = wall_speed

        space_for_walls = Window.height - self.gap_size

        top_wall_height_occupation = (random.randint(1, 9) / 10) * space_for_walls
        bottom_wall_height_occupation = space_for_walls - top_wall_height_occupation

        self.bottom_wall.widget.pos = (self.initial_bottom_wall_pos[0], 0)
        self.bottom_wall.widget.size = (self.wall_width, bottom_wall_height_occupation)

        self.top_wall.widget.pos = (self.initial_top_wall_pos[0], Window.height - top_wall_height_occupation)
        self.top_wall.widget.size = (self.wall_width, top_wall_height_occupation)

    def reset_walls(self):
        self.bottom_wall.reset()
        self.top_wall.reset()
