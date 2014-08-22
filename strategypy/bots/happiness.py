import random
import sys
from copy import deepcopy

from api import BaseBot

from happines_base import Bot as HappinessBaseBot


"""
...........
.....3.....
....323....
...32123...
..321H123..
...32X23...
....323....
.....3.....
...........
...........
...........
"""


class Bot(HappinessBaseBot):
    

    def calc_happiness(self, friend_dist, enemy_dist):
        # row is distance, value is happiness based on num bots there

        happiness = 0. #+ random.random()/100.

        if friend_dist[0] or enemy_dist[0]:
            return happiness

        for distance in range(1, 100):

            max_per_shell = 4 * distance
            shell_occupancy = (friend_dist[distance] * 1. / max_per_shell)
            happiness += min(shell_occupancy, 0.74) / distance

        return happiness
