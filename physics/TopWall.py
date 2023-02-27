from physics.Wall import Wall


class TopWall(Wall):
    def __init__(self, widget, initial_pos, initial_size):
        super().__init__(widget, initial_pos, initial_size)
