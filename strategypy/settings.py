"""
All the settings/constants of the game
"""

GRID_SIZE = (50, 50)
UNITS = 51
MAX_TURNS = 1000

try:
    from local_settings import *
except ImportError:
    pass
