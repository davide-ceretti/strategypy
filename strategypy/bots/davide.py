import uuid
import random

from api import BaseBot


class Bot(BaseBot):
    positions = {}

    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)
        self.uuid = uuid.uuid4()
        self.went_down = False

    def action(self):
        """
        Always move LEFT or RIGHT to match the avg X of other cells
        """
        x, y = self.position
        self.positions[self.uuid] = self.position

        numb_bots = len(self.positions)
        avg_x = sum(x for x, _ in self.positions.itervalues())/numb_bots

        if self.position == self.previous_position and avg_x != x:
            if self.went_down:
                # I tried to go down before but I got stuck
                self.went_down = False
                return 'move {}'.format(random.choice(['up', 'left', 'right']))
            self.went_down = True
            return 'move down'

        self.went_down = False
        if x > avg_x:
            return 'move left'
        elif x < avg_x:
            return 'move right'
        else:
            return 'move up'
