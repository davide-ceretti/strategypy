import json
import itertools
import operator
import random
import os.path
import sys
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from strategypy.game import Game
from strategypy.bots.davide import Bot as DavideBot
from strategypy import settings

settings.GRID_SIZE = (30, 30)
settings.UNITS = 10
settings.MAX_TURNS = 100
settings.RESPAWN = False
settings.BORDER = "WALL"

_ORIGINAL_RULES = DavideBot.rules
ORIGINAL_RULES = [
    _ORIGINAL_RULES['risk_of_dieing'],
    _ORIGINAL_RULES['outnumber_isolated_enemies'],
    _ORIGINAL_RULES['closer_to_central_mass'],
    _ORIGINAL_RULES['find_isolated_targets'],
]


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
    utility = len(davide_units) * is_davide_winner

    return utility


def play_games(rules, n=5):
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
    return tuple(round(random.random(), 2) for _ in xrange(0, 4))


def make_son(rules_one, rules_two):
    son = [
        random.choice([a, b])
        for a, b in zip(rules_one, rules_two)
    ]

    # Mutation
    if random.random() < 0.1:
        random_id = random.randint(0, 3)
        val = son[random_id]
        new_val = val + random.uniform(-0.2, 0.2)
        if new_val < 0:
            new_val = 0
        elif new_val > 1:
            new_val = 1
        son[random_id] = round(new_val, 2)

    return tuple(son)


def weighted_random_parent(parents_list):
    # Square weights
    weights = [x**2 for _, x in parents_list]
    rnd = random.random() * sum(weights)
    for rule, value in parents_list:
        rnd -= value ** 2
        if rnd < 0:
            return rule, value


def random_parents(parents_list):
    parents = parents_list[:]
    first = weighted_random_parent(parents)
    parents.remove(first)
    second = weighted_random_parent(parents)
    return first[0], second[0]


# TRAININGS

def custom_training(rule=None):
    GAMES_TO_PLAY = 200

    if rule is None:
        rule = ORIGINAL_RULES

    result = play_games(rule, n=GAMES_TO_PLAY)

    print 'Played {} games with rule {}: {}'.format(
        GAMES_TO_PLAY, rule, result)

    return rule


def bruteforce_training():
    GAMES_TO_PLAY = 10

    values = set()
    values.update(set(itertools.permutations([10, 10, 10, 1])))
    values.update(set(itertools.permutations([10, 10, 5, 1])))
    values.update(set(itertools.permutations([10, 10, 1, 1])))
    values.update(set(itertools.permutations([10, 5, 5, 1])))
    values.update(set(itertools.permutations([10, 5, 2, 1])))
    values.update(set(itertools.permutations([10, 5, 1, 1])))
    values.update(set(itertools.permutations([10, 1, 1, 1])))
    values.update(set(itertools.permutations([2, 1, 1, 1])))
    values.update(set(itertools.permutations([2, 2, 2, 1])))
    values.update(set(itertools.permutations([2, 2, 1, 1])))
    values.update(set(itertools.permutations([3, 3, 3, 1])))
    values.update(set(itertools.permutations([3, 3, 2, 1])))
    values.update(set(itertools.permutations([3, 3, 1, 1])))
    values.update(set(itertools.permutations([1, 1, 1, 1])))

    n = len(values)
    print 'BRUTEFORCE TRAINING - {} rules'.format(n)
    result = {}
    for i, value in enumerate(values):
        result[value] = play_games(value, n=GAMES_TO_PLAY)
        per_cent = (i*100)/float(n)
        print '{:.1f}% - Played {} games with rule {}: {}'.format(
            per_cent, GAMES_TO_PLAY, value, result[value])
    return max_from_dict(result)


def random_training():
    GAMES_TO_PLAY = 10
    values = [random_rules() for _ in xrange(0, 100)]

    n = len(values)
    print 'RANDOM TRAINING - {} rules'.format(n)
    result = {}
    for i, value in enumerate(values):
        result[value] = play_games(value, n=GAMES_TO_PLAY)
        per_cent = (i*100)/float(n)
        print '{:.1f}% - Played {} games with rule {}: {}'.format(
            per_cent, GAMES_TO_PLAY, value, result[value])
    return max_from_dict(result)


def genetic_algorithms_training():
    SONS = 10
    PARENTS = 20
    RANDOM = 20
    GENETIC_POOL = SONS + PARENTS + RANDOM
    GAMES_TO_PLAY = 300
    GENERATIONS = 50
    print 'RANDOM TRAINING - {} rules, {} generations'.format(
        GENETIC_POOL, GENERATIONS)
    print
    values = [random_rules() for _ in xrange(0, GENETIC_POOL)]
    for j in xrange(0, GENERATIONS):
        result = {}
        print 'Start generation {}'.format(j)
        for i, value in enumerate(values):
            result[value] = play_games(value, n=GAMES_TO_PLAY)
            per_cent =  \
                (100*(j*GENETIC_POOL + i))/float(GENERATIONS * GENETIC_POOL)
            print '{:.1f}% - Played {} games with rule {}: {}'.format(
                per_cent, GAMES_TO_PLAY, value, result[value])

        parents = []
        for i in xrange(0, PARENTS):
            rule = max_from_dict(result)
            result.pop(rule[0])
            parents.append(rule)
        avg = round(sum(x for __, x in parents)/PARENTS, 2)
        print 'Average of best {} rules for generation {} is: {}'.format(
            PARENTS, j, avg)
        print

        sons = [
            make_son(*random_parents(parents))
            for _ in xrange(0, SONS)
        ]

        values = [
            random_rules()
            for _ in xrange(0, RANDOM)
        ]
        values.extend([x for x, __ in parents])
        values.extend(sons)

    return parents[0]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "trainer",
        choices=['bruteforce', 'genetic', 'random', 'custom']
    )
    funcs = {
        'bruteforce': bruteforce_training,
        'genetic': genetic_algorithms_training,
        'random': random_training,
        'custom': custom_training,
    }
    arguments = parser.parse_args()
    print funcs[arguments.trainer]()
