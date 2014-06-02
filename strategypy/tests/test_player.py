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


@patch('core.game.settings.COLORS', COLORS)
@patch('core.game.settings.DEFAULT_COLOR_NAME', DEFAULT_COLOR_NAME)
class TestPlayerSetColorAndName(unittest.TestCase):
    def setUp(self):
        Player.__init__ = lambda *args: None
        self.player = Player()

    def test_color_in_colors(self):
        self.player.pk = 2

        self.player.set_color_and_name()

        self.assertEqual(self.player.name, 'blue')
        self.assertEqual(self.player.color, pygame.Color(0, 0, 255))

    def test_color_not_in_colors(self):
        self.player.pk = 6

        self.player.set_color_and_name()

        self.assertEqual(self.player.name, '???')
        self.assertEqual(self.player.color, pygame.Color(100, 100, 100))


class TestPlayerGetBotClassModuleName(unittest.TestCase):
    def setUp(self):
        Player.__init__ = lambda *args: None
        self.player = Player()

    def test_imported_bot(self):
        from bots.test_one import Bot
        self.player.bot_class = Bot

        module_name = self.player.get_bot_class_module_name()

        self.assertEqual(module_name, 'test_one')
