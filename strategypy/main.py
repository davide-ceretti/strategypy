import os
import sys
import pygame

from core.game import Game
import settings

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.display.set_mode(settings.SCREEN_SIZE)
    game = Game(*sys.argv[1:])
    game.main_loop()
    pygame.quit()
    sys.exit()
