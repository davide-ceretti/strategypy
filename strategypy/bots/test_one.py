"""
Bot used in unittests
"""
from api import BaseBot


class Bot(BaseBot):
    def action(self):
        return 'move up'
