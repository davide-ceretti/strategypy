from mock import patch
import unittest

from players import Unit


@patch('game.consts.GRID_SIZE', (3, 4))
class TestUnitMove(unittest.TestCase):
    """
    The grid should look like this
    (0, 0) (1, 0) (2, 0)
    (0, 1) (1, 1) (2, 1)
    (0, 2) (1, 2) (2, 2)
    (0, 3) (1, 3) (2, 3)
    """
    def setUp(self):
        self.unit = Unit(None)

    def test_move_nonsense(self):
        self.unit.x = 1
        self.unit.y = 1

        self.unit.move('nonsense')

        self.assertEqual(self.unit.x, 1)
        self.assertEqual(self.unit.y, 1)

    def test_move_up(self):
        self.unit.x = 1
        self.unit.y = 1

        self.unit.move('up')

        self.assertEqual(self.unit.x, 1)
        self.assertEqual(self.unit.y, 0)

    def test_move_up_not_allowed(self):
        self.unit.x = 1
        self.unit.y = 0

        self.unit.move('up')

        self.assertEqual(self.unit.x, 1)
        self.assertEqual(self.unit.y, 0)

    def test_move_left(self):
        self.unit.x = 1
        self.unit.y = 1

        self.unit.move('left')

        self.assertEqual(self.unit.x, 0)
        self.assertEqual(self.unit.y, 1)

    def test_move_left_not_allowed(self):
        self.unit.x = 0
        self.unit.y = 2

        self.unit.move('left')

        self.assertEqual(self.unit.x, 0)
        self.assertEqual(self.unit.y, 2)

    def test_move_down(self):
        self.unit.x = 1
        self.unit.y = 1

        self.unit.move('down')

        self.assertEqual(self.unit.x, 1)
        self.assertEqual(self.unit.y, 2)

    def test_move_down_not_allowed(self):
        self.unit.x = 1
        self.unit.y = 3

        self.unit.move('down')

        self.assertEqual(self.unit.x, 1)
        self.assertEqual(self.unit.y, 3)

    def test_move_right(self):
        self.unit.x = 1
        self.unit.y = 1

        self.unit.move('right')

        self.assertEqual(self.unit.x, 2)
        self.assertEqual(self.unit.y, 1)

    def test_move_right_not_allowed(self):
        self.unit.x = 2
        self.unit.y = 2

        self.unit.move('right')

        self.assertEqual(self.unit.x, 2)
        self.assertEqual(self.unit.y, 2)
