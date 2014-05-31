import random
from api import BaseBot


class Bot(BaseBot):
    def action(self):
        if self.position[1] == 0:
            return
        moved = not self.position == self.previous_position
        where = 'up' if moved else random.choice(['down', 'left', 'right'])
        return 'move {}'.format(where)
