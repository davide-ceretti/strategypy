from api import BaseBot


class Bot(BaseBot):
    def action(self, ctx):
        return 'move right'
