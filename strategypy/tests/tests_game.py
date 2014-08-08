import unittest
from mock import Mock, patch

from game import Game
from components import Player, Unit
from api import BaseBot


# TODO: Do not patch __init__, do not Mock

@patch.object(Game, "__init__", side_effect=lambda *args: None)
class TestInitPlayers(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.occupied_cells = set()

    def test_no_bots(self, init):
        self.game.bots = []
        self.game.init_players()
        self.assertListEqual(self.game.players, [])

    def test_multiple_bots(self, init):
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


@patch.object(Game, "__init__", side_effect=lambda *args: None)
class TestInitBots(unittest.TestCase):
    def setUp(self):
        Game.__init__ = lambda x: None
        self.game = Game()

    def test_no_args(self, init):
        self.game.args = []
        self.game.init_bots()
        self.assertListEqual(self.game.bots, [])

    def test_one_bot(self, init):
        self.game.args = ['test_one']
        self.game.init_bots()
        from bots.test_one import Bot
        self.assertListEqual(self.game.bots, [Bot])


@patch.object(Game, "__init__", side_effect=lambda *args: None)
class TestUpdateOccupiedCells(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.occupied_cells = set()

    def test_update_occupied_cells(self, init):
        player_one = Mock(spec=Player)
        player_two = Mock(spec=Player)
        player_one.units = [
            Mock(spec=Unit, current_cell=(1, 3), pk=1),
            Mock(spec=Unit, current_cell=(2, 4), pk=2),
        ]
        player_two.units = [
            Mock(spec=Unit, current_cell=(3, 5), pk=1),
            Mock(spec=Unit, current_cell=(4, 6), pk=2),
        ]

        self.game.players = [player_one, player_two]

        self.game.auto_update_occupied_cells()

        expected = {(1, 3), (2, 4), (3, 5), (4, 6)}
        self.assertSetEqual(self.game.occupied_cells, expected)


@patch.object(Game, "__init__", side_effect=lambda *args: None)
class TestSnapshotData(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.data = ['initial_data']

    def test_snapshot_data(self, init):
        player_one = Mock(spec=Player, pk=12)
        player_two = Mock(spec=Player, pk=99)
        player_one.units = [
            Mock(spec=Unit, current_cell=(1, 3), pk=1),
            Mock(spec=Unit, current_cell=(2, 4), pk=2),
        ]
        player_two.units = [
            Mock(spec=Unit, current_cell=(3, 5), pk=1),
            Mock(spec=Unit, current_cell=(4, 6), pk=2),
        ]

        self.game.players = [player_one, player_two]

        self.game.snapshot_data()

        expected_data = {
            12: {
                1: (1, 3),
                2: (2, 4),
            },
            99: {
                1: (3, 5),
                2: (4, 6)
            }
        }
        expected = ['initial_data', expected_data]
        self.assertListEqual(self.game.data, expected)
