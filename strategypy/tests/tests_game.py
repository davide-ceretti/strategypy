import unittest
from mock import patch, call, Mock

from core.game import Game
from core.players import Player, Unit
from api import BaseBot
import settings


@patch('core.game.pygame')
class TestGameDrawGrid(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        Game.__init__ = lambda x: None
        self.game = Game()
        self.game.screen = None

    @patch('core.game.settings.SCREEN_SIZE', (6, 4))
    @patch('core.game.settings.UNIT_SIZE', (2, 2))
    def test_2x3(self, pg):
        self.game.draw_grid()
        calls = [
            call(None, settings.GRID_COLOR, (0, 0), (0, 4), 1),
            call(None, settings.GRID_COLOR, (2, 0), (2, 4), 1),
            call(None, settings.GRID_COLOR, (4, 0), (4, 4), 1),
            call(None, settings.GRID_COLOR, (6, 0), (6, 4), 1),
            call(None, settings.GRID_COLOR, (0, 0), (6, 0), 1),
            call(None, settings.GRID_COLOR, (0, 2), (6, 2), 1),
            call(None, settings.GRID_COLOR, (0, 4), (6, 4), 1),
        ]
        self.assertListEqual(calls, pg.draw.line.call_args_list)


class TestGameDraw(unittest.TestCase):
    def setUp(self):
        Game.__init__ = lambda x: None
        Game.units = []  # We override the property
        self.game = Game()
        self.game.screen = Mock()
        self.game.draw_grid = Mock()

    def test_game_draw_no_units(self):
        self.game.units = []

        self.game.draw()

        self.assertEqual(self.game.draw_grid.call_count, 1)
        self.game.screen.fill.assert_called_once_with(settings.BG_COLOR)

    def test_game_draw_multiple_units(self):
        self.game.units = [Mock(), Mock(), Mock()]

        self.game.draw()

        self.assertEqual(self.game.draw_grid.call_count, 1)
        self.game.screen.fill.assert_called_once_with(settings.BG_COLOR)
        for unit in self.game.units:
            self.assertEqual(unit.render.call_count, 1)


class TestInitPlayers(unittest.TestCase):
    def setUp(self):
        Game.__init__ = lambda x: None
        self.game = Game()
        self.game.occupied_cells = []

    def test_no_bots(self):
        self.game.bots = []
        self.game.init_players()
        self.assertListEqual(self.game.players, [])

    def test_multiple_bots(self):
        class BotOne(BaseBot):
            pass

        class BotTwo(BaseBot):
            pass

        self.game.bots = [BotOne, BotTwo]

        self.game.init_players()

        first_player, second_player = self.game.players
        self.assertEqual(first_player.pk, 0)
        self.assertEqual(first_player.bot_class, BotOne)
        self.assertIsInstance(first_player, Player)
        self.assertEqual(second_player.pk, 1)
        self.assertEqual(second_player.bot_class, BotTwo)
        self.assertIsInstance(second_player, Player)


class TestInitBots(unittest.TestCase):
    def setUp(self):
        Game.__init__ = lambda x: None
        self.game = Game()

    def test_no_args(self):
        self.game.args = []
        self.game.init_bots()
        self.assertListEqual(self.game.bots, [])

    def test_one_bot(self):
        self.game.args = ['test_one']
        self.game.init_bots()
        from bots.test_one import Bot
        self.assertListEqual(self.game.bots, [Bot])


class TestCheckForVictory(unittest.TestCase):
    def setUp(self):
        Game.__init__ = lambda x: None
        self.game = Game()

    def test_game_already_finished(self):
        player = Mock(spec=Player)
        self.game.victorious_player = player

        self.game.check_for_victory()

        self.assertEqual(self.game.victorious_player, player)

    def test_no_winners(self):
        player_one = Mock(spec=Player)
        player_one.units = [
            Mock(spec=Unit, current_cell=(1, 3)),
            Mock(spec=Unit, current_cell=(2, 4)),
        ]
        self.game.victorious_player = None
        self.game.players = [player_one]

        self.game.check_for_victory()

        self.assertIsNone(self.game.victorious_player)

    def test_winner_horizontal(self):
        player_one = Mock(spec=Player)
        player_one.units = [
            Mock(spec=Unit, current_cell=(1, 3)),
            Mock(spec=Unit, current_cell=(2, 3)),
        ]
        self.game.victorious_player = None
        self.game.players = [player_one]

        self.game.check_for_victory()

        self.assertEqual(self.game.victorious_player, player_one)

    def test_winner_vertical(self):
        player_one = Mock(spec=Player)
        player_one.units = [
            Mock(spec=Unit, current_cell=(1, 3)),
            Mock(spec=Unit, current_cell=(1, 2)),
        ]
        self.game.victorious_player = None
        self.game.players = [player_one]

        self.game.check_for_victory()

        self.assertEqual(self.game.victorious_player, player_one)
