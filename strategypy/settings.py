"""
All the settings/constants of the game
"""

GRID_SIZE = (30, 30)
UNITS = 20
MAX_TURNS = 150

WIN_DIFF = 5

try:
    from local_settings import *
except ImportError:
    pass
