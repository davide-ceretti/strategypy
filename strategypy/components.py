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
        self.pk = pk
        self.has_killed = []
        self.was_killed_by = []

        self.ctx = {
            'player_pk': self.player.pk,
            'pk': self.pk,
            'respawn': settings.RESPAWN,
            'grid_size': settings.GRID_SIZE,
        }

        self.bot = player.bot_class(self.ctx)

    def action(self):
        """
        Call the action method defined in the bot
        """
        ctx = self.assemble_ctx_for_bot()
        direction = self.bot.__process_action__(ctx)
        self.move(direction)

    def assemble_ctx_for_bot(self):
        ctx = {
            'current_data': self.player.game.current_data(),
            'has_killed': [(u.player.pk, u.pk) for u in self.has_killed],
            'was_killed_by': [(u.player.pk, u.pk) for u in self.was_killed_by],
            'position': self.current_cell,
        }

        ctx.update(self.ctx)

        return ctx

    def notify_has_killed(self, unit):
        self.has_killed.append(unit)

    def notify_was_killed_by(self, units):
        self.was_killed_by = units

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

        if settings.BORDER == 'WALL':
            inside = movement['condition']
            x = self.x + movement['dx']
            y = self.y + movement['dy']
            free = (x, y) not in self.player.game.occupied_cells
            if inside and free:
                self.x = x
                self.y = y

        if settings.BORDER == 'WRAP':
            x = (self.x + movement['dx']) % X
            y = (self.y + movement['dy']) % Y
            free = (x, y) not in self.player.game.occupied_cells
            if free:
                self.x = x
                self.y = y

    def spawn_random(self):
        """
        Move the Unit to a random position on the grid
        """
        self.place_randomly()
        # FIXME: As we are still creating players at this point we have
        # To update occupied_cells manually
        self.player.game.occupied_cells[(self.x, self.y)] = self

    def get_random_location(self):
        X, Y = settings.GRID_SIZE
        all_cells = {(x, y) for x in xrange(0, X) for y in xrange(0, Y)}
        occupied_cells = self.player.game.occupied_cells
        open_cells = all_cells - set(occupied_cells.keys())
        return random.sample(open_cells, 1)[0]

    def place_randomly(self):
        self.x, self.y = self.get_random_location()

    @property
    def current_cell(self):
        return (self.x, self.y)
