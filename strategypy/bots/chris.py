import math
import random
from api import BaseBot


class Bot(BaseBot):
    """Chris' Bot"""
    circle_radius = random.randint(16, 64)

    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)
        self.number_of_actions = random.randint(0, 32)

    def action(self):
        '''Move in a circular fashion
        '''
        self.number_of_actions += 1
        a = 2 * math.sin((self.number_of_actions % self.circle_radius) * math.pi/(self.circle_radius/2))
        directions = (
            (-2, -1, 'move down'),
            (-1, 0, 'move left'),
            (0, 1, 'move up'),
            (1, 2, 'move right'),
        )
        for direction in directions:
            _min, _max, _dir = direction

            if _min <= a <= _max:
                return _dir
