import random
from api import BaseBot

DIRECTIONS = ('up', 'down', 'left', 'right')


class Bot(BaseBot):
    direction = random.choice(DIRECTIONS)

    @property
    def happy_condition(self):
        x, y = self.position
        X, Y = self.grid_size
        conditions = {
            'up': y == 0,
            'down': y == Y - 1,
            'left': x == 0,
            'right': x == X - 1,
        }
        return conditions[self.direction]

    def action(self):
        if self.happy_condition:
            return
        moved = not self.position == self.previous_position
        chosen_move = random.choice(DIRECTIONS)
        where = self.direction if moved else chosen_move
        return 'move {}'.format(where)
