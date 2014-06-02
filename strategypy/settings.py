"""
All the settings/constants of the game
"""
import pygame

# Screen & grid
CAPTION = "StrategyPY"
FPS = 10
BG_COLOR = (0, 0, 0)
SCREEN_SIZE = (800, 600)
UNIT_SIZE = (10, 10)
GRID_SIZE = tuple(x/y for x, y in zip(SCREEN_SIZE, UNIT_SIZE))
GRID_COLOR = (50, 50, 50)
u_x, u_y = UNIT_SIZE
cell = lambda x, y: (u_x*x, u_y*y, u_x, u_y)

# Colors

DEFAULT_COLOR_NAME = ('???', pygame.Color(100, 100, 100))
COLORS = {
    0: ('red', pygame.Color(255, 0, 0)),
    1: ('green', pygame.Color(0, 255, 0)),
    2: ('blue', pygame.Color(0, 0, 255)),
    3: ('yellow', pygame.Color(255, 255, 0)),
    4: ('cyanic', pygame.Color(0, 255, 255)),
    5: ('fucsia', pygame.Color(255, 0, 255)),
}

# Gameplay
UNITS = 50

try:
    from local_settings import *
except ImportError:
    pass
