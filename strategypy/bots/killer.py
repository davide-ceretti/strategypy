import random

from api import BaseBot


class Bot(BaseBot):
    pray = {}

    def action(self):
        current_frame = self.current_data
        if 'unit' in self.pray and 'player' in self.pray:
            if self.pray['unit'] not in current_frame.get(self.pray['player'], []):
                self.pray.pop('unit')
                self.pray.pop('player')

        choices = current_frame.keys()
        choices.remove(self.player_pk)
        if not 'player' in self.pray:
            self.pray['player'] = random.choice(choices)
        if not 'unit' in self.pray:
            self.pray['unit'] = random.choice(
                current_frame[self.pray['player']].keys()
            )

        # Chase the target
        x, y = self.position
        tx, ty = current_frame[self.pray['player']][self.pray['unit']]
        dx = x - tx
        dy = y - ty
        if dx == 0:
            direction = 'down' if dy < 0 else 'up'
            return 'move {}'.format(direction)
        if dy == 0:
            direction = 'right' if dx < 0 else 'left'
            return 'move {}'.format(direction)
        choice = random.choice(['x', 'y'])
        if choice == 'x':
            direction = 'right' if dx < 0 else 'left'
            return 'move {}'.format(direction)
        else:
            direction = 'down' if dy < 0 else 'up'
            return 'move {}'.format(direction)
