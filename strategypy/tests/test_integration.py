"""
The purpose of this module is to test the game end to end
by using some custom bots.
"""

import unittest
import json
import itertools

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


@patch.object(settings, 'UNITS', 1)
@patch.object(settings, 'MAX_TURNS', 3)
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
    def assertUnitMoved(self, game, player_pk, direction, unit_pk='0'):
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

        self.assertUnitMoved(result, '1', 'up')

    def test_cant_move_up_occupied(self, get_random_location):
        locations = [(5, 4), (5, 5)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_moveup')

        self.assertUnitMoved(result, '1', None)

    def test_cant_move_up_on_border(self, get_random_location):
        locations = [(5, 5), (6, 0)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_moveup')

        self.assertUnitMoved(result, '1', None)

    def test_can_move_down(self, get_random_location):
        locations = [(0, 0), (5, 5)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_movedown')

        self.assertUnitMoved(result, '1', 'down')

    def test_cant_move_down_occupied(self, get_random_location):
        locations = [(5, 6), (5, 5)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_movedown')

        self.assertUnitMoved(result, '1', None)

    def test_cant_move_down_on_border(self, get_random_location):
        locations = [(5, 5), (6, 9)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_movedown')

        self.assertUnitMoved(result, '1', None)

    def test_can_move_left(self, get_random_location):
        locations = [(0, 0), (5, 5)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_moveleft')

        self.assertUnitMoved(result, '1', 'left')

    def test_cant_move_left_occupied(self, get_random_location):
        locations = [(5, 5), (6, 5)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_moveleft')

        self.assertUnitMoved(result, '1', None)

    def test_cant_move_left_border(self, get_random_location):
        locations = [(5, 5), (0, 9)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_moveleft')

        self.assertUnitMoved(result, '1', None)

    def test_can_move_right(self, get_random_location):
        locations = [(0, 0), (5, 5)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_moveright')

        self.assertUnitMoved(result, '1', 'right')

    def test_cant_move_right_occupied(self, get_random_location):
        locations = [(6, 5), (5, 5)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_moveright')

        self.assertUnitMoved(result, '1', None)

    def test_cant_move_right_border(self, get_random_location):
        locations = [(5, 5), (9, 1)]
        get_random_location.side_effect = locations

        result = play_game('unittest_static', 'unittest_moveright')

        self.assertUnitMoved(result, '1', None)


@patch.object(settings, 'UNITS', 2)
@patch.object(settings, 'MAX_TURNS', 10)
@patch.object(settings, 'GRID_SIZE', (2, 6))
@patch.object(Unit, 'get_random_location')
class TestKilling(unittest.TestCase):
    locations = (
        (0, 0), (0, 3),  # Player zero
        (0, 5), (1, 5),  # Player one
    )
    """
    The game should look like this. Read horizontally
      0   1   2   3   4
    ---------------------
    |0 X|0 X|0 X|0 X|X X|
    |X X|X X|X X|X X|1 1|
    |X X|X X|X X|1 1|X X|
    |0 X|X X|1 1|X X|X X|
    |X X|1 1|1 1|1 1|1 1|
    |1 1|X X|X X|X X|X X|
    ---------------------
    """
    def test_move_up_is_winner(self, get_random_location):
        get_random_location.side_effect = self.locations

        result = play_game('unittest_static', 'unittest_moveup')

        winner = result['winner']
        self.assertEqual(winner, 1)

    def test_static_units_are_killed(self, get_random_location):
        get_random_location.side_effect = self.locations

        result = play_game('unittest_static', 'unittest_moveup')

        # Player zero has two units at frame zero
        units = result['frames'][0]['0'].keys()
        self.assertEqual(len(units), 2)

        # Player zero has one unit at frame one
        units = result['frames'][1]['0'].keys()
        self.assertEqual(len(units), 1)

        # Player zero loses at frame four
        players = result['frames'][4].keys()
        self.assertNotIn('0', players)


@patch.object(settings, 'UNITS', 4)
@patch.object(settings, 'MAX_TURNS', 1)
@patch.object(settings, 'GRID_SIZE', (3, 4))
class TestSpawning(unittest.TestCase):
    def test_units_are_spawned_in_different_cells(self):
        """
        Randomly spawns 12 units in 12 cells
        """
        result = play_game(
            'unittest_static', 'unittest_static', 'unittest_static'
        )

        units = itertools.chain(
            *[unit.values() for unit in result['frames'][0].values()]
        )
        units = sorted(list(units))

        expected = [[x, y] for x in xrange(3) for y in xrange(4)]
        self.assertListEqual(units, expected)
