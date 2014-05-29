import random
import pygame

import settings


class Player(object):
    """
    It represents a player in the game
    """
    def __init__(self, pk, action_func, game):
        self.pk = pk
        self.game = game
        self.units = [Unit(self) for _ in xrange(settings.UNITS)]
        self.color = self.set_color()
        self.action_func = action_func

    def action(self):
        """
        Execute the dynamic action functions for all its units
        """
        for unit in self.units:
            self.action_func(unit)

    def set_color(self):  # TODO: Make it a proper setter
        """
        Assign a color to the player
        """
        grey = pygame.Color(100, 100, 100)
        colors = {
            0: pygame.Color(255, 0, 0),
            1: pygame.Color(0, 255, 0),
            2: pygame.Color(0, 0, 255),
            3: pygame.Color(175, 175, 0),
        }
        return colors.get(self.pk, grey)


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

    @property
    def current_cell(self):
        return (self.x, self.y)
