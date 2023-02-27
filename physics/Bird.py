from physics.PhysicsObject import PhysicsObject


class Bird(PhysicsObject):
    jump_vertical_force = 500

    def __init__(self, widget, initial_pos, initial_size):
        super().__init__(widget, initial_pos, initial_size)

    def jump(self):
        self.vertical_velocity = 0
        self.add_vertical_velocity(self.jump_vertical_force)

    def reset(self):
        self.widget.pos = self.initial_pos
        self.vertical_velocity = 0
        self.horizontal_velocity = 0
