from physics.Point import Point


class PhysicsObject:
    widget = None
    mass = 1
    vertical_velocity = 0
    horizontal_velocity = 0
    initial_pos = (0, 0)
    initial_size = (0, 0)

    def __init__(self, widget, initial_pos, initial_size):
        self.widget = widget
        self.initial_pos = initial_pos
        self.initial_size = initial_size

    def add_vertical_velocity(self, force):
        self.vertical_velocity += force

    def add_horizontal_velocity(self, force):
        self.horizontal_velocity += force

    def transition(self, dt):
        self.widget.pos = (self.widget.pos[0] + dt * self.horizontal_velocity,
                           self.widget.pos[1] + dt * self.vertical_velocity)

    def is_colliding_with(self, pos, size):
        l1 = Point(self.widget.pos[0], self.widget.pos[1] + self.widget.size[1])
        r1 = Point(self.widget.pos[0] + self.widget.size[0], self.widget.pos[1])
        l2 = Point(pos[0], pos[1] + size[1])
        r2 = Point(pos[0] + size[0], pos[1])

        if l1.x == r1.x or l1.y == r1.y:
            return False

        if r2.x == l2.x or l2.y == r2.y:
            return False

        if l1.x > r2.x or l2.x > r1.x:
            return False

        if r1.y > l2.y or r2.y > l1.y:
            return False

        return True
