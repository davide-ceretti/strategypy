import unittest
from mock import Mock, patch

from api import BaseBot
from components import Unit


class TestBaseBot(unittest.TestCase):
    def setUp(self):
        self.mocked_player = Mock(pk=1)
        self.mocked_unit = Mock(spec=Unit, player=self.mocked_player, pk=1)
        self.base_bot = BaseBot(self.mocked_unit)

    def test_init(self):
        self.assertEqual(self.base_bot.__unit__, self.mocked_unit)

    def test_action(self):
        with self.assertRaises(NotImplementedError):
            self.base_bot.action()

    def test___process_action__not_allowed(self):
        self.base_bot.action = lambda: "unallowed action"
        self.base_bot.__allowed_actions__ = ['move up']

        self.base_bot.__process_action__()

        has_moved = self.base_bot.__unit__.move.called
        self.assertFalse(has_moved)

    def test___process_action__allowed(self):
        self.base_bot.action = lambda: "move up"
        self.base_bot.__allowed_actions__ = ['move up']

        self.base_bot.__process_action__()

        has_moved = self.base_bot.__unit__.move.called
        self.assertTrue(has_moved)

    def test___process_action__updating_prev_position(self):
        self.base_bot.__previous_position__ = (2, 1)
        self.mocked_unit.current_cell = (1, 1)
        self.base_bot.action = lambda: "move up"
        self.base_bot.__allowed_actions__ = ['move up']

        self.base_bot.__process_action__()

        self.assertEqual(self.base_bot.__previous_position__, (1, 1))

    def test_position(self):
        self.mocked_unit.current_cell = (9, 6)
        self.assertTupleEqual(self.base_bot.position, (9, 6))

    def test_previous_position(self):
        self.base_bot.__previous_position__ = (3, 5)
        self.assertTupleEqual(self.base_bot.previous_position, (3, 5))

    @patch('api.settings.GRID_SIZE', (13, 37))
    def test_grid_size(self):
        grid_size = self.base_bot.grid_size
        self.assertEqual(grid_size, (13, 37))
