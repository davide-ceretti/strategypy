import random

from api import BaseBot


class Bot(BaseBot):
    def action(self, ctx):
        actions = [
            'move up',
            'move left',
            'move right',
            'move down',
        ]
        return random.choice(actions)
