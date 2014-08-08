from mock import patch
import unittest

from components import Player

# TODO: Stop patching __init__ for fuck sake


@patch.object(Player, "__init__", side_effect=lambda *args: None)
class TestPlayerGetBotClassModuleName(unittest.TestCase):
    def test_imported_bot(self, init):
        from bots.test_one import Bot
        self.player = Player()
        self.player.bot_class = Bot

        module_name = self.player.get_bot_class_module_name()

        self.assertEqual(module_name, 'test_one')
