import json
import itertools
import operator
import random
import os.path
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from game import Game
from bots.davide import Bot as DavideBot
import settings

settings.GRID_SIZE = (15, 15)
settings.UNITS = 10
settings.MAX_TURNS = 75
settings.RESPAWN = False
settings.BORDER = "WALL"


def play_game(rules):
    a, b, c, d = rules
    rules_dict = {
        'be_able_to_move': 100.0,
        'risk_of_dieing': a,
        'outnumber_isolated_enemies': b,
        'closer_to_central_mass': c,
        'find_isolated_targets': d,
    }
    DavideBot.rules = rules_dict

    game = Game('davide', 'happiness')
    result = game.main_loop()
    result = json.loads(result)

    davide_units = result['frames'][-1].get('0', [])
    is_davide_winner = result['winner'] == 0
    turns = result['turns']
    utility = len(davide_units) * is_davide_winner
    if utility > 0:
        utility += 1 - (turns/float(settings.MAX_TURNS))

    return utility


def play_games(rules, n=20):
    results = [play_game(rules) for _ in xrange(0, n)]
    avg = sum(results)/float(len(results))
    return avg


def max_from_dict(dictionary):
    k, v = max(
        dictionary.iteritems(),
        key=operator.itemgetter(1)
    )
    return k, v


def random_rules():
    return tuple(random.random() * 2 for _ in xrange(0, 4))


def make_son(rules_one, rules_two):
    son = list(
        (a + b)/float(2)
        for a, b in zip(rules_one, rules_two)
    )
    # Mutate son
    for each in son:
        mutation = random.random() / 5
        new_val = each - 0.1 + mutation
        if new_val > 0:
            each += new_val

    return tuple(son)


# TRAININGS


def bruteforce_training():
    values = []
    values += itertools.permutations([10, 10, 10, 1])
    values += itertools.permutations([10, 10, 5, 1])
    values += itertools.permutations([10, 10, 1, 1])
    values += itertools.permutations([10, 5, 5, 1])
    values += itertools.permutations([10, 5, 2, 1])
    values += itertools.permutations([10, 5, 1, 1])
    values += itertools.permutations([10, 1, 1, 1])
    values += itertools.permutations([2, 1, 1, 1])
    values += itertools.permutations([2, 2, 2, 1])
    values += itertools.permutations([2, 2, 1, 1])
    values += itertools.permutations([3, 3, 3, 1])
    values += itertools.permutations([3, 3, 2, 1])
    values += itertools.permutations([3, 3, 1, 1])
    values += itertools.permutations([1, 1, 1, 1])

    result = {
        value: play_games(value)
        for value in values
    }
    return max_from_dict(result)


def random_training():
    values = [random_rules() for _ in xrange(0, 50)]
    result = {
        value: play_games(value)
        for value in values
    }
    return max_from_dict(result)


def genetic_algorythms_training():
    AMOUNT_OF_SONS = 8
    GENETIC_POOL = 40
    values = [random_rules() for _ in xrange(0, GENETIC_POOL)]
    for i, x in enumerate(xrange(0, 50)):
        result = {
            value: play_games(value)
            for value in values
        }
        k_one, v_one = max_from_dict(result)
        result.pop(k_one)
        k_two, v_two = max_from_dict(result)
        sons = [make_son(k_one, k_two) for _ in xrange(0, AMOUNT_OF_SONS)]
        values = [
            random_rules()
            for _ in xrange(0, GENETIC_POOL - AMOUNT_OF_SONS)
        ]
        values.extend([k_one, k_two])
        values.extend(sons)
        print 'Best of {} generation: {} {} '.format(i, k_one, v_one)

    return k_one, v_one

if __name__ == '__main__':
    print bruteforce_training()
    print genetic_algorythms_training()
    print random_training()
