import random
import operator

from api import BaseBot


class Bot(BaseBot):
    actions = {
        'move up': (0, -1),
        'move right': (1, 0),
        'move down': (0, 1),
        'move left': (-1, 0),
        None: (0, 0),
    }

    rules = {
        'be_able_to_move': 0.1,
        'risk_of_dieing': 0.01,
        'closer_to_central_mass': 0.001,
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

        chosen = max(
            weighted_actions.iteritems(),
            key=operator.itemgetter(1)
        )[0]
        return chosen

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
        if x == 0:
            result['move left'] = 0.0
        if x == X - 1:
            result['move right'] = 0.0
        if y == 0:
            result['move up'] = 0.0
        if y == Y - 1:
            result['move down'] = 0.0
        return result

    def closer_to_central_mass(self, ctx):
        board = ctx['current_data']
        pk = ctx['player_pk']
        x, y = ctx['position']
        allies = board[pk].values()
        n = len(allies)
        avg_x = sum(x for x, _ in allies)/n
        avg_y = sum(y for _, y in allies)/n
        dx = x - avg_x
        dy = y - avg_y
        # TODO: Optimize
        result = {
            'move up': float(abs(dx) <= abs(dy) and dy >= 0),
            'move down': float(abs(dx) <= abs(dy) and dy < 0),
            'move left': float(abs(dx) > abs(dy) and dx >= 0),
            'move right': float(abs(dx) > abs(dy) and dx < 0),
            None: 0.0
        }
        return result

    def risk_of_dieing(self, ctx):
        board = ctx['current_data']
        pk = ctx['player_pk']
        x, y = ctx['position']
        enemies = [v.values() for k, v in board.iteritems() if k != pk][0]

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

            number_of_dangerous_enemies = len(dangerous_enemies)
            result[k] = 1.0 - (number_of_dangerous_enemies/20.0)
        return result
