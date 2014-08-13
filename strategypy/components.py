import random

import settings


class Player(object):
    """
    A player in the game.
    """
    def __init__(self, pk, bot_class, game):
        self.pk = pk
        self.game = game
        self.bot_class = bot_class
        self.units = [Unit(self, i) for i in xrange(settings.UNITS)]
        self.has_killed = {}
        self.was_killed_by = {}

    def get_bot_class_module_name(self):
        """
        Returns the name of the module we imported
        bot_class from
        """
        _, module_name = self.bot_class.__module__.split('.')
        return module_name


class Unit(object):
    """
    A single unit controlled by a Player. It's represented
    on the game grid by a small coloured square.
    """
    def __init__(self, player, pk):
        self.x = 0
        self.y = 0
        self.player = player
        self.spawn_random()
        self.bot = player.bot_class(self)
        self.pk = pk

    def action(self):
        """
        Call the action method defined in the bot
        """
        self.bot.__process_action__()

    def move(self, direction):
        """
        Move the unit up, down, left or right
        """
        X, Y = settings.GRID_SIZE
        up = {
            'condition': self.y > 0,
            'dx': 0,
            'dy': -1,
        }

        down = {
            'condition': self.y < Y - 1,
            'dx': 0,
            'dy': 1,
        }

        left = {
            'condition': self.x > 0,
            'dx': -1,
            'dy': 0,
        }

        right = {
            'condition': self.x < X - 1,
            'dx': 1,
            'dy': 0,
        }

        possible_movements = {
            'left': left,
            'right': right,
            'up': up,
            'down': down,
        }

        movement = possible_movements.get(direction, None)
        if movement is None:
            return
        inside = movement['condition']
        x = self.x + movement['dx']
        y = self.y + movement['dy']
        free = (x, y) not in self.player.game.occupied_cells
        if inside and free:
            self.x = x
            self.y = y

    def spawn_random(self):
        """
        Move the Unit to a random position on the grid
        """
        X, Y = settings.GRID_SIZE
        all_cells = {(x, y) for x in xrange(0, X) for y in xrange(0, Y)}
        occupied_cells = self.player.game.occupied_cells
        open_cells = all_cells - occupied_cells
        self.x, self.y = random.sample(open_cells, 1)[0]
        # FIXME: As we are still creating players at this point we have
        # To update occupied_cells manually
        occupied_cells.add((self.x, self.y))

    @property
    def current_cell(self):
        return (self.x, self.y)
