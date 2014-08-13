"""
The purpose of this module is to test the game end to end
by using some custom bots.
"""

import unittest
import json

from game import Game
import settings

# Patch settings
settings.GRID_SIZE = (10, 10)
settings.UNITS = 3
settings.MAX_TURNS = 20
settings.RESPAWN = False


class TestGame(unittest.TestCase):
    def play_game(self, *args):
        game = Game(*args)
        result = game.main_loop()
        return json.loads(result)

    def mock_place_randomly(self, units):
        def place_unit(unit, *args, **kwargs):
            for pk, units in units.items():
                if unit.player.pk == pk:
                    unit.x, unit.y = units.pop()
        return place_unit

    def test_game_can_run(self):
        result = self.play_game('unittest_static', 'unittest_moveup')
        self.assertIsNotNone(result)

    def test_player_info(self):
        result = self.play_game('unittest_static', 'unittest_static')

        player_zero_data = {
            'has_killed': {},
            'name': 'unittest_static',
            'was_killed_by': {},
        }
        player_one_data = {
            'has_killed': {},
            'name': 'unittest_static',
            'was_killed_by': {},
        }
        expected = {
            '0': player_zero_data,
            '1': player_one_data,
        }

        self.assertDictEqual(result['all_players'], expected)

    def test_no_winner(self):
        result = self.play_game('unittest_static', 'unittest_static')
        self.assertIsNone(result['winner'])

    def test_grid_info(self):
        result = self.play_game('unittest_static', 'unittest_static')
        self.assertListEqual(result['grid_size'], [10, 10])
