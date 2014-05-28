import os
import sys
import pygame

from game import Game
from consts import SCREEN_SIZE

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.display.set_mode(SCREEN_SIZE)
    game = Game(*sys.argv[1:])
    game.main_loop()
    pygame.quit()
    sys.exit()
