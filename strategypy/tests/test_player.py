from mock import patch
import unittest
import pygame

from core.players import Player

DEFAULT_COLOR_NAME = ('???', pygame.Color(100, 100, 100))
COLORS = {
    0: ('red', pygame.Color(255, 0, 0)),
    1: ('green', pygame.Color(0, 255, 0)),
    2: ('blue', pygame.Color(0, 0, 255)),
    3: ('yellow', pygame.Color(255, 255, 0)),
    4: ('cyanic', pygame.Color(0, 255, 255)),
    5: ('fucsia', pygame.Color(255, 0, 255)),
}

# TODO: Stop patching __init__, fuck isolation


@patch('core.game.settings.COLORS', COLORS)
@patch('core.game.settings.DEFAULT_COLOR_NAME', DEFAULT_COLOR_NAME)
@patch.object(Player, "__init__", side_effect=lambda *args: None)
class TestPlayerSetColorAndName(unittest.TestCase):
    def test_color_in_colors(self, init):
        self.player = Player()
        self.player.pk = 2

        self.player.set_color_and_name()

        self.assertEqual(self.player.name, 'blue')
        self.assertEqual(self.player.color, pygame.Color(0, 0, 255))

    def test_color_not_in_colors(self, init):
        self.player = Player()
        self.player.pk = 6

        self.player.set_color_and_name()

        self.assertEqual(self.player.name, '???')
        self.assertEqual(self.player.color, pygame.Color(100, 100, 100))


@patch.object(Player, "__init__", side_effect=lambda *args: None)
class TestPlayerGetBotClassModuleName(unittest.TestCase):
    def test_imported_bot(self, init):
        from bots.test_one import Bot
        self.player = Player()
        self.player.bot_class = Bot

        module_name = self.player.get_bot_class_module_name()

        self.assertEqual(module_name, 'test_one')
