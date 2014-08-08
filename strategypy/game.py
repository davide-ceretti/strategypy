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
        self.occupied_cells = {unit.current_cell for unit in self.units}

    def init_players(self):
        """
        Create Players and load their personal bot
        """
        # I can't initialize players with a list comprehension because
        # Player __init__ need to access Game.players attribute
        # TODO: Code smell?
        self.players = []
        for i, bot_class in enumerate(self.bots):
            player = Player(i, bot_class, self)
            self.players.append(player)

    def init_bots(self):
        """
        Create bot action functions by getting the name of the
        package/module from the args
        """
        for arg in self.args:
            __import__('bots.{}'.format(arg))
        self.bots = [getattr(bots, arg).Bot for arg in self.args]

    def snapshot_data(self):
        snapshot = {}
        for player in self.players:
            snapshot[player.pk] = {}
            for unit in player.units:
                snapshot[player.pk][unit.pk] = unit.current_cell
        self.data.append(snapshot)

    def build_json_data(self):
        players = {
            player.pk: player.get_bot_class_module_name()
            for player in self.players
        }
        winner = self.get_winner()
        data = {
            'frames': self.data,
            'winner': None if winner is None else winner.pk,
            'turns': self.counter,
            'players': players,
            'grid_size': settings.GRID_SIZE,
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
        def is_blocked(position):
            X, Y = settings.GRID_SIZE
            x, y = position
            a = position in self.occupied_cells
            # Outside the grid
            b = x < 0 or x >= X
            c = y < 0 or y >= Y
            return a or b or c

        to_be_removed = []

        for unit in self.units:
            x, y = unit.current_cell
            blocked = 0
            for xd, yd in (
                (0, 1), (1, 0), (0, -1), (-1, 0)
            ):
                ox = x + xd
                oy = y + yd
                if is_blocked((ox, oy)):
                    blocked += 1

            if blocked == 4:
                to_be_removed.append(unit)

        for unit in to_be_removed:
            unit.player.units.remove(unit)


    # def get_winner(self):
    #     """
    #     Determine whether the game has ended or not and
    #     return the victorious_player accordingly.
    #     Condition of victory: all the units should be aligned
    #     either vertically or horizontaly
    #     """
    #     for player in self.players:
    #         positions = [unit.current_cell for unit in player.units]
    #         xs = set(x for x, y in positions)
    #         ys = set(y for x, y in positions)
    #         if len(xs) == 1 or len(ys) == 1:
    #             # We have a winner :)
    #             return player

    def get_winner(self):
        min_units = min(len(player.units) for player in self.players)
        for player in self.players:
            if len(player.units) - min_units > settings.WIN_DIFF:
                return player

    def main_loop(self):
        """
        The main loop of the game, can be interrupted by events
        """
        self.counter = 0
        winner = None
        while self.counter < settings.MAX_TURNS and winner is None:
            self.update()
            winner = self.get_winner()
            self.snapshot_data()
            self.counter += 1
        # import ipdb; ipdb.set_trace()
        sys.stdout.write(self.build_json_data())
