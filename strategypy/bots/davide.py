import random

from api import BaseBot


class Bot(BaseBot):
    actions = {
        'move up': (0, -1),
        'move right': (1, 0),
        'move down': (0, 1),
        'move left': (-1, 0),
        None: (0, 0),
    }

    def get_available_moves(self, ctx):
        open_directions = self.actions.copy()
        x, y = ctx['position']
        X, Y = ctx['grid_size']
        if x == 0:
            open_directions.pop('move left')
        if x == X - 1:
            open_directions.pop('move right')
        if y == 0:
            open_directions.pop('move up')
        if y == Y - 1:
            open_directions.pop('move down')
        return open_directions

    def action(self, ctx):
        moves = self.get_available_moves(ctx).keys()
        action_matrix = {
            k: self.how_close_am_i_to_die_if_i_went(ctx, k)
            for k in moves
        }

        min_value = action_matrix[min(action_matrix)]
        keys = [k for k, v in action_matrix.iteritems() if v == min_value]
        return self.get_best_direction(ctx, keys)

    def get_best_direction(self, ctx, directions):
        board = ctx['current_data']
        pk = ctx['player_pk']
        x, y = ctx['position']
        allies = board[pk].values()
        n = len(allies)
        avg_x = sum(x for x, _ in allies)/n
        avg_y = sum(y for _, y in allies)/n
        dx = x - avg_x
        dy = y - avg_y
        if abs(dx) > abs(dy):
            best = 'move left' if dx > 0 else 'move right'
        else:
            best = 'move up' if dy > 0 else 'move down'
        if best in directions:
            return best
        else:
            return random.choice(directions)

    def how_close_am_i_to_die_if_i_went(self, ctx, direction):
        board = ctx['current_data']
        pk = ctx['player_pk']
        x, y = ctx['position']
        enemies = [v.values() for k, v in board.iteritems() if k != pk][0]
        """
        0 is danger, 1 is current unit
        (3, 4)
        X X X X X X X
        X X X X X X X
        X X 0 0 0 X X
        X 0 0 0 0 0 X
        X 0 0 1 0 0 X
        X 0 0 0 0 0 X
        X X 0 0 0 X X
        X X X X X X X
        """
        x_offset, y_offset = self.actions[direction]

        x_initial = x - 2 + x_offset
        x_final = x + 2 + x_offset
        y_initial = y - 2 + y_offset
        y_final = y + 2 + y_offset
        danger_values = [
            (p, q)
            for p in xrange(x_initial, x_final + 1)
            for q in xrange(y_initial, y_final + 1)
        ]
        danger_values.remove((x_initial, y_initial))  # Top left
        danger_values.remove((x_final, y_initial))  # Top right
        danger_values.remove((x_initial, y_final))  # Bottom left
        danger_values.remove((x_final, y_final))  # Bottom right

        dangerous_enemies = [each for each in enemies if each in danger_values]

        return len(dangerous_enemies)/float(20)
