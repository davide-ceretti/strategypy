from api import BaseBot

DIRECTIONS = ('up', 'down', 'left', 'right')



class Bot(BaseBot):

    def __init__(self, unit):
        super(Bot, self).__init__(unit)

        self.last_move = None
        self.target_id = (0, 0)
        self.axis = 0
        self.last_stuck = False
        self.previous_position = None
        self.saved = []

    def action(self, ctx):
        if self.reached_target(ctx):
            self.cycle_target()

        self.last_move = self.get_direction(ctx)
        self.previous_position = ctx['position']
        if self.last_move:
            return 'move {}'.format(self.last_move)

    def reached_target(self, ctx):
        return ctx['position'] == self.get_target(ctx)

    def get_direction(self, ctx):
        target = self.get_target(ctx)

        self.stuck = self.previous_position == ctx['position'] and not (self.last_move is None)
        if self.stuck:
            if self.last_stuck and not self.saved:
                self.saved = []
                self.saved.append('right' if target[0] < ctx['position'][0] else 'left')
                self.saved.append('down' if target[1] < ctx['position'][1] else 'up')
            self.axis = 1 if self.axis is 0 else 1
            self.last_stuck = True
        elif self.axis == 0 and ctx['position'][0] == target[0]:
            self.axis = 1
        elif self.axis == 1 and ctx['position'][1] == target[1]:
            self.axis = 0
        if not self.stuck:
            self.last_stuck = False

        if self.saved:
            return self.saved.pop(0)

        if target[self.axis] < ctx['position'][self.axis]:
            return 'left' if self.axis == 0 else 'up'
        elif target[self.axis] > ctx['position'][self.axis]:
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

    def get_target(self, ctx):
        if self.target_id[0] == 0:
            x = int(ctx['grid_size'][0] * 0.1)
        else:
            x = ctx['grid_size'][0] - int(ctx['grid_size'][0] * 0.1)
        if self.target_id[1] == 0:
            y = int(ctx['grid_size'][1] * 0.1)
        else:
            y = ctx['grid_size'][1] - int(ctx['grid_size'][1] * 0.1)
        return x, y

