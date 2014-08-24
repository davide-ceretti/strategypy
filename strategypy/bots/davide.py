import operator

from api import BaseBot


# Utilities

def max_from_dict(dictionary):
    result = max(
        dictionary.iteritems(),
        key=operator.itemgetter(1)
    )[0]
    return result


def get_me_closer_to(ctx, my_position, their_position):
    my_x, my_y = my_position
    their_x, their_y = their_position
    X, Y = ctx['grid_size']
    X, Y = float(X), float(Y)
    dx = my_x - their_x
    dy = my_y - their_y

    move_up = 1 - (Y - dy)/Y if dy > 0 else 0.0
    move_down = 1 - (Y + dy)/Y if dy < 0 else 0.0
    move_left = 1 - (X - dx)/X if dx > 0 else 0.0
    move_right = 1 - (X + dx)/X if dx < 0 else 0.0

    result = {
        'move up': move_up,
        'move down': move_down,
        'move left': move_left,
        'move right': move_right,
        None: 0.0
    }
    return result


class Bot(BaseBot):
    actions = {
        'move up': (0, -1),
        'move right': (1, 0),
        'move down': (0, 1),
        'move left': (-1, 0),
        None: (0, 0),
    }

    # Optimized for 1v1 vs Happines
    # On (15, 15) grid with 10 units
    # Using bruteforce_training
    rules = {
        'be_able_to_move': 100.0,
        'risk_of_dieing': 2,
        'outnumber_isolated_enemies': 1,
        'closer_to_central_mass': 3,
        'find_isolated_targets': 3,
    }

    def action(self, ctx):
        rules_actions = {
            rule: getattr(self, rule)(ctx)
            for rule in self.rules.iterkeys()
        }
        weighted_actions = {
            action: self._eval_weighted_action(action, rules_actions)
            for action in self.actions
        }

        return max_from_dict(weighted_actions)

    # UTILS

    def _eval_weighted_action(self, action, rules_actions):
        value = sum(
            v * rules_actions[k][action]
            for k, v in self.rules.iteritems()
        )
        return value

    # RULES

    def be_able_to_move(self, ctx):
        result = {k: 1.0 for k in self.actions.iterkeys()}
        x, y = ctx['position']
        X, Y = ctx['grid_size']
        board = ctx['current_data']
        occupied_cells = [v.values() for k, v in board.iteritems()][0]
        try:
            occupied_cells.remove((x, y))
        except ValueError:
            pass
        if x == 0 or (x-1, y) in occupied_cells:
            result['move left'] = 0.0
        if x == X - 1 or (x+1, y) in occupied_cells:
            result['move right'] = 0.0
        if y == 0 or (x, y-1) in occupied_cells:
            result['move up'] = 0.0
        if y == Y - 1 or (x, y+1) in occupied_cells:
            result['move down'] = 0.0
        return result

    def closer_to_central_mass(self, ctx):
        board = ctx['current_data']
        pk = ctx['player_pk']
        my_position = ctx['position']
        allies = board[pk].values()
        n = len(allies)
        avg_position = (
            sum(x for x, _ in allies)/n,
            sum(y for _, y in allies)/n
        )

        result = get_me_closer_to(ctx, my_position, avg_position)
        return result

    def outnumber_isolated_enemies(self, ctx):
        board = ctx['current_data']
        pk = ctx['player_pk']
        my_position = ctx['position']
        x, y = my_position
        allies = board[pk].values()
        enemies = [v.values() for k, v in board.iteritems() if k != pk][0]
        close_allies = sum(
            1
            for ax, ay in allies
            if abs(x-ax) <= 3 and abs(y-ay) <= 3
        )
        close_enemies = [
            (ex, ey)
            for ex, ey in enemies
            if abs(x-ex) <= 6 and abs(y-ey) <= 6
        ]

        n = len(close_enemies)
        if not n:
            return {k: 1.0 for k in self.actions.keys()}

        avg_position = (
            sum(x for x, _ in close_enemies)/n,
            sum(y for _, y in close_enemies)/n
        )

        result = get_me_closer_to(ctx, my_position, avg_position)

        if close_allies >= len(close_enemies):
            return result
        else:
            return {k: 1.0 - v for k, v in result.iteritems()}

    def find_isolated_targets(self, ctx):
        board = ctx['current_data']
        pk = ctx['player_pk']
        my_position = ctx['position']
        enemies = [v.values() for k, v in board.iteritems() if k != pk][0]
        n = len(enemies)
        avg_enemies_x = sum(x for x, _ in enemies)/n
        avg_enemies_y = sum(y for _, y in enemies)/n
        distances_from_avg = {
            (ex, ey): abs(ex - avg_enemies_x) + abs(ey - avg_enemies_y)
            for ex, ey in enemies
        }

        target_position = max_from_dict(distances_from_avg)
        result = get_me_closer_to(ctx, my_position, target_position)

        return result

    def risk_of_dieing(self, ctx):
        board = ctx['current_data']
        pk = ctx['player_pk']
        x, y = ctx['position']
        enemies = [v.values() for k, v in board.iteritems() if k != pk][0]
        allies = board[pk].values()

        result = {}
        for k, v in self.actions.iteritems():
            x_offset, y_offset = v

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

            dangerous_enemies = [
                each
                for each in enemies
                if each in danger_values
            ]
            allies_in_danger_values = [
                each
                for each in allies
                if each in danger_values
            ]

            number_of_dangerous_enemies = len(dangerous_enemies)
            number_of_allies = len(allies_in_danger_values)
            diff = number_of_allies - number_of_dangerous_enemies
            if diff > 0:
                result[k] = 1.0
            else:
                result[k] = 1.0 + (diff/len(danger_values))
        return result
