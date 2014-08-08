"""
All the settings/constants of the game
"""

GRID_SIZE = (80, 60)
UNITS = 20
MAX_TURNS = 1000

try:
    from local_settings import *
except ImportError:
    pass
