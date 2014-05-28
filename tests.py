import unittest
from mock import patch, call

from game import Game
import consts


@patch('game.pygame')
class TestGameDrawGrid(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        Game.__init__ = lambda x: None
        self.game = Game()
        self.game.screen = None

    @patch('game.consts.SCREEN_SIZE', (6, 4))
    @patch('game.consts.UNIT_SIZE', (2, 2))
    def test_2x3(self, pg):
        self.game.draw_grid()
        calls = [
            call(None, consts.GRID_COLOR, (0, 0), (0, 4), 1),
            call(None, consts.GRID_COLOR, (2, 0), (2, 4), 1),
            call(None, consts.GRID_COLOR, (4, 0), (4, 4), 1),
            call(None, consts.GRID_COLOR, (6, 0), (6, 4), 1),
            call(None, consts.GRID_COLOR, (0, 0), (6, 0), 1),
            call(None, consts.GRID_COLOR, (0, 2), (6, 2), 1),
            call(None, consts.GRID_COLOR, (0, 4), (6, 4), 1),
        ]
        self.assertListEqual(calls, pg.draw.line.call_args_list)

if __name__ == '__main__':
    unittest.main()
