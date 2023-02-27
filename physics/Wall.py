from physics.PhysicsObject import PhysicsObject


class Wall(PhysicsObject):
    initial_horizontal_speed = -250
    horizontal_velocity = initial_horizontal_speed

    def __init__(self, widget, initial_pos, initial_size):
        super().__init__(widget, initial_pos, initial_size)

    def reset(self):
        self.widget.pos = self.initial_pos
        self.widget.size = self.initial_size
