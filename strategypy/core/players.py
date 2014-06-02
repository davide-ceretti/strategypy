import random
import pygame

import settings


class Player(object):
    """
    A player in the game.
    """
    def __init__(self, pk, bot_class, game):
        self.pk = pk
        self.game = game
        self.bot_class = bot_class
        self.units = [Unit(self) for _ in xrange(settings.UNITS)]
        self.set_color_and_name()

    def set_color_and_name(self):
        """
        Assign a color and a name to the player
        """
        name, color = settings.COLORS.get(self.pk, settings.DEFAULT_COLOR_NAME)
        self.color = color
        self.name = name

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
    def __init__(self, player):
        self.x = 0
        self.y = 0
        self.player = player
        self.spawn_random()
        self.bot = player.bot_class(self)

    def action(self):
        """
        Call the action method defined in the bot
        """
        self.bot.__process_action__()

    def render(self):
        """
        Render the unit on the grid
        """
        surface = pygame.display.get_surface()
        pygame.draw.rect(
            surface, self.player.color, settings.cell(self.x, self.y)
        )

    def move(self, direction):
        """
        Move the unit up, down, left or right
        """
        up = {
            'condition': self.y > 0,
            'dx': 0,
            'dy': -1,
        }

        down = {
            'condition': self.y < settings.GRID_SIZE[1] - 1,
            'dx': 0,
            'dy': 1,
        }

        left = {
            'condition': self.x > 0,
            'dx': -1,
            'dy': 0,
        }

        right = {
            'condition': self.x < settings.GRID_SIZE[0] - 1,
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
        # TODO: Optimize
        x, y = settings.GRID_SIZE
        retry = True
        while retry:
            x_candidate = random.randint(0, x)
            y_candidate = random.randint(0, y)
            if (self.x, self.y) not in self.player.game.occupied_cells:
                self.x = x_candidate
                self.y = y_candidate
                retry = False
        self.player.game.set_occupied_cells()

    @property
    def current_cell(self):
        return (self.x, self.y)
