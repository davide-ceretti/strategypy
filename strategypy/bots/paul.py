from api import BaseBot

DIRECTIONS = ('up', 'down', 'left', 'right')



class Bot(BaseBot):

    def __init__(self, unit):
        super(Bot, self).__init__(unit)

        self.last_move = None
        self.target_id = (0, 0)
        self.axis = 0
        self.last_stuck = False
        self.saved = []

    def action(self):
        if self.reached_target():
            self.cycle_target()

        self.last_move = self.get_direction()
        if self.last_move:
            return 'move {}'.format(self.last_move)

    def reached_target(self):
        return self.position == self.get_target()

    def get_direction(self):
        target = self.get_target()

        self.stuck = self.previous_position == self.position and not (self.last_move is None)
        if self.stuck:
            if self.last_stuck and not self.saved:
                self.saved = []
                self.saved.append('right' if target[0] < self.position[0] else 'left')
                self.saved.append('down' if target[1] < self.position[1] else 'up')
            self.axis = 1 if self.axis is 0 else 1
            self.last_stuck = True
        elif self.axis == 0 and self.position[0] == target[0]:
            self.axis = 1
        elif self.axis == 1 and self.position[1] == target[1]:
            self.axis = 0
        if not self.stuck:
            self.last_stuck = False

        if self.saved:
            return self.saved.pop(0)

        if target[self.axis] < self.position[self.axis]:
            return 'left' if self.axis == 0 else 'up'
        elif target[self.axis] > self.position[self.axis]:
            return 'right' if self.axis == 0 else 'down'
        else:
            self.cycle_target()

    def cycle_target(self):
        if self.target_id == (0, 0):
            self.target_id = (1, 0)
        elif self.target_id == (0, 1):
            self.target_id = (1, 0)
        elif self.target_id == (1, 0):
            self.target_id = (1, 1)
        elif self.target_id == (1, 1):
            self.target_id = (0, 0)

    def get_target(self):
        if self.target_id[0] == 0:
            x = int(self.grid_size[0] * 0.1)
        else:
            x = self.grid_size[0] - int(self.grid_size[0] * 0.1)
        if self.target_id[1] == 0:
            y = int(self.grid_size[1] * 0.1)
        else:
            y = self.grid_size[1] - int(self.grid_size[1] * 0.1)
        return x, y

