import random

pray = {}


def action(ctx):
    current_frame = ctx['current_data']
    player_pk = ctx['player_pk']
    if 'unit' in pray and 'player' in pray:
        if pray['unit'] not in current_frame.get(pray['player'], []):
            pray.pop('unit')
            pray.pop('player')

    choices = current_frame.keys()
    choices.remove(player_pk)
    if not 'player' in pray:
        pray['player'] = random.choice(choices)
    if not 'unit' in pray:
        pray['unit'] = random.choice(
            current_frame[pray['player']].keys()
        )

    # Chase the target
    x, y = ctx['position']
    tx, ty = current_frame[pray['player']][pray['unit']]
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
