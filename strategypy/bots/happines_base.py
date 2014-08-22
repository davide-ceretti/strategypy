import random
import sys
from copy import deepcopy

from api import BaseBot



class Bot(BaseBot):
    
    MAX_DIST = 100

    distance_template = {}

    directions = {
        'move up': (0, -1),
        'move right': (1, 0),
        'move down': (0, 1),
        'move left': (-1, 0),
        None: (0, 0),
    }

    distance_template = {}

    for direction in directions:
        distance_template[direction] = {}
        for bot_type in ['friends', 'enemies']:
            distance_template[direction][bot_type] = [0] * MAX_DIST


    def _get_distances(self, ctx):
        current_frame = ctx['current_data']
        player_pk = ctx['player_pk']
        pk = ctx['pk']
        x, y = ctx['position']

        distances = deepcopy(self.distance_template)
        for other_player_pk, units in current_frame.items():
            
            if other_player_pk == player_pk:
                bot_type = 'friends'
            else:
                bot_type = 'enemies'

            for unit_pk, (ox, oy) in units.items():
                
                for direction, (dx, dy) in self.directions.items():
                    dist = abs((x +  dx) - ox) + abs((y + dy) - oy)
                    
                    if dist >= self.MAX_DIST:
                        continue

                    distances[direction][bot_type][dist] += 1

        return distances

    def calc_happiness(self, friend_dist, enemy_dist):
        raise NotImplementedError

    def _calc_happiness(self, directions):
        
        res = []

        for direction in directions:
            happiness = self.calc_happiness(directions[direction]['friends'], directions[direction]['enemies'])
            res.append((happiness, direction))
  
        max_hap = max(res)[0]

        return random.choice([d for h,d in res if h == max_hap])
            
        return happiest[0]


    def action(self, ctx):
        dist = self._get_distances(ctx)
        return self._calc_happiness(dist)
