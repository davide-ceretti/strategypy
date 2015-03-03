import sys

from game import Game


def run():
    game = Game(*sys.argv[1:])
    result = game.main_loop()
    sys.stdout.write(result)
