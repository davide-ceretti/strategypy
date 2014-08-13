"""
All the settings/constants of the game
"""

GRID_SIZE = (40, 40)
UNITS = 10
MAX_TURNS = 3000
RESPAWN=False

try:
    from local_settings import *
except ImportError:
    pass
