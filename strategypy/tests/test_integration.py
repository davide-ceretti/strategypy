"""
The purpose of this module is to test the game end to end
by using some custom bots.
"""

import unittest
import json

from mock import patch

from game import Game
from components import Unit
import settings


def play_game(*args):
    game = Game(*args)
    result = game.main_loop()
    return json.loads(result)


@patch.object(settings, 'MAX_TURNS', 10)
class TestGameCanRun(unittest.TestCase):
    def test_game_can_run_three_players(self):
        args = [
            'unittest_static', 'unittest_moveup', 'unittest_moveleft',
        ]
        result = play_game(*args)
        self.assertIsNotNone(result)


@patch.object(settings, 'UNITS', 3)
@patch.object(settings, 'MAX_TURNS', 5)
@patch.object(settings, 'GRID_SIZE', (10, 10))
class TestGameOutput(unittest.TestCase):
    def test_player_info(self):
        result = play_game('unittest_static', 'unittest_static')

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
        result = play_game('unittest_static', 'unittest_static')
        self.assertIsNone(result['winner'])

    def test_grid_info(self):
        result = play_game('unittest_static', 'unittest_static')
        self.assertListEqual(result['grid_size'], [10, 10])


@patch.object(settings, 'UNITS', 1)
@patch.object(settings, 'MAX_TURNS', 2)
@patch.object(settings, 'GRID_SIZE', (10, 10))
@patch.object(Unit, 'get_random_location')
class TestMovement(unittest.TestCase):
    def assert_moved(self, game, player_pk, direction, unit_pk='0'):
        """
        Assert that the unit moved in the given direction in their
        first action
        """
        diffs = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0),
            None: (0, 0),
        }
        xa, ya = game['frames'][0][player_pk]['0']
        xb, yb = game['frames'][1][player_pk]['0']
        diff_x, diff_y = diffs[direction]
        self.assertEqual(yb-ya, diff_y)
        self.assertEqual(xb-xa, diff_x)

    def test_can_move_up(self, get_random_location):
        locations = [(0, 0), (5, 5)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_moveup')

        self.assert_moved(result, '1', 'up')

    def test_cant_move_up_occupied(self, get_random_location):
        locations = [(5, 4), (5, 5)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_moveup')

        self.assert_moved(result, '1', None)

    def test_cant_move_up_on_border(self, get_random_location):
        locations = [(5, 5), (6, 0)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_moveup')

        self.assert_moved(result, '1', None)

    def test_can_move_down(self, get_random_location):
        locations = [(0, 0), (5, 5)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_movedown')

        self.assert_moved(result, '1', 'down')

    def test_cant_move_down_occupied(self, get_random_location):
        locations = [(5, 6), (5, 5)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_movedown')

        self.assert_moved(result, '1', None)

    def test_cant_move_down_on_border(self, get_random_location):
        locations = [(5, 5), (6, 9)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_movedown')

        self.assert_moved(result, '1', None)

    def test_can_move_left(self, get_random_location):
        locations = [(0, 0), (5, 5)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_moveleft')

        self.assert_moved(result, '1', 'left')

    def test_cant_move_left_occupied(self, get_random_location):
        locations = [(5, 5), (6, 5)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_moveleft')

        self.assert_moved(result, '1', None)

    def test_cant_move_left_border(self, get_random_location):
        locations = [(5, 5), (0, 9)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_moveleft')

        self.assert_moved(result, '1', None)

    def test_can_move_right(self, get_random_location):
        locations = [(0, 0), (5, 5)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_moveright')

        self.assert_moved(result, '1', 'right')

    def test_cant_move_right_occupied(self, get_random_location):
        locations = [(6, 5), (5, 5)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_moveright')

        self.assert_moved(result, '1', None)

    def test_cant_move_right_border(self, get_random_location):
        locations = [(5, 5), (9, 1)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_moveright')

        self.assert_moved(result, '1', None)
