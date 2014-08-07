import sys

from core.game import Game

if __name__ == "__main__":
    game = Game(*sys.argv[1:])
    game.main_loop()
