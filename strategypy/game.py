from random import shuffle
import json
import sys

import bots
import settings
from components import Player


class Game(object):
    def __init__(self, *args):
        self.args = args
        self.data = []
        self.occupied_cells = set()
        self.init_bots()
        self.init_players()

    def auto_update_occupied_cells(self):
        """
        Update the list of the cells currently occupied by units
        """
        # TODO: Optimize by adding add update_occupied_cells instead
        self.occupied_cells = {unit.current_cell: unit for unit in self.units}

    def init_players(self):
        """
        Create Players and load their personal bot
        """
        # I can't initialize players with a list comprehension because
        # Player __init__ need to access Game.players attribute
        # TODO: Code smell?
        self.players = []
        self.all_players = []
        for i, bot_class in enumerate(self.bots):
            player = Player(i, bot_class, self)
            self.players.append(player)
            self.all_players.append(player)

    def init_bots(self):
        """
        Create bot action functions by getting the name of the
        package/module from the args
        """
        for arg in self.args:
            __import__('bots.{}'.format(arg))
        self.bots = [getattr(bots, arg).Bot for arg in self.args]

    def snapshot_data(self):
        snapshot = self.current_data()
        self.data.append(snapshot)

    def current_data(self):
        snapshot = {}
        for player in self.players:
            snapshot[player.pk] = {}
            for unit in player.units:
                snapshot[player.pk][unit.pk] = unit.current_cell
        return snapshot

    def build_json_data(self):
        players = {
            player.pk: player.get_bot_class_module_name()
            for player in self.players
        }

        all_players = {
            player.pk: {
                'name': player.get_bot_class_module_name(),
                'has_killed': {
                    killed.get_bot_class_module_name(): num_times
                    for killed, num_times in player.has_killed.items()
                },
            }
            for player in self.all_players
        }
        
        winner = self.get_winner()
        data = {
            'frames': self.data,
            'winner': None if winner is None else winner.pk,
            'turns': self.counter,
            'players': players,
            'grid_size': settings.GRID_SIZE,
            'all_players': all_players
        }
        return json.dumps(data)

    @property
    def units(self):
        """
        All the units in the Game
        """
        return (unit for player in self.players for unit in player.units)

    def update(self):
        """
        Fetch all unit positions and action units
        """
        units = list(self.units)
        shuffle(units)
        for unit in units:
            unit.action()
            self.auto_update_occupied_cells()
        self.kill_units()
        self.auto_update_occupied_cells()

    def kill_units(self):
        current_data = self.current_data()

        def is_outnumbered(unit, player_pk):
            x, y = unit.current_cell
            player_units = current_data[player_pk].values()

            killers = []

            allies, enemies = 0, 0
            for xd in xrange(-1, 2):
                for yd in xrange(-1, 2):
                    ox = x + xd
                    oy = y + yd

                    if is_outside(ox, oy):
                        continue

                    if (ox, oy) not in self.occupied_cells:
                        continue

                    if (ox, oy) in player_units:
                        allies += 1
                    else:
                        enemies += 1
                        killers.append(self.occupied_cells[(ox, oy)])

            return enemies > allies, killers

        def is_outside(x, y):
            X, Y = settings.GRID_SIZE
            # Outside the grid
            a = x < 0 or x >= X
            b = y < 0 or y >= Y
            return a or b

        to_be_removed = []

        for unit in self.units:
            x, y = unit.current_cell
            to_remove, killer_units = is_outnumbered(unit, unit.player.pk)

            if to_remove:
                to_be_removed.append(unit)
      
                # update the players stats
                killer_players = {unit.player for unit in killer_units}
                for killer_player in killer_players:

                    # increment the killers 
                    killer_player.has_killed.setdefault(unit.player, 0)
                    killer_player.has_killed[unit.player] += 1
                    
                    # and the killee 
                    unit.player.was_killed_by.setdefault(killer_player, 0)
                    unit.player.was_killed_by[killer_player] += 1

        for unit in to_be_removed:
            unit.player.units.remove(unit)

        to_be_removed = [
            player for player in self.players
            if len(player.units) == 0
        ]
        for player in to_be_removed:
            self.players.remove(player)

    def get_winner(self):
        alive = [player for player in self.players if len(player.units) > 0]
        if len(alive) == 1:
            return alive[0]

    def main_loop(self):
        """
        The main loop of the game, can be interrupted by events
        """
        self.snapshot_data()
        self.counter = 0
        winner = None
        while self.counter < settings.MAX_TURNS and winner is None:
            self.update()
            winner = self.get_winner()
            self.snapshot_data()
            self.counter += 1
        sys.stdout.write(self.build_json_data())
