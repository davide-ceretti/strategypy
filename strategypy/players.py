import random
import pygame

import consts


class Player(object):
    def __init__(self, pk, action_func):
        self.pk = pk
        self.units = [Unit(self) for _ in xrange(consts.UNITS)]
        self.color = self.get_color()
        self.action_func = action_func

    def action(self):
        for unit in self.units:
            self.action_func(unit)

    def get_color(self):
        grey = pygame.Color(100, 100, 100)
        colors = {
            0: pygame.Color(255, 0, 0),
            1: pygame.Color(0, 255, 0),
            2: pygame.Color(0, 0, 255),
            3: pygame.Color(175, 175, 0),
        }
        return colors.get(self.pk, grey)


class Unit(object):
    def __init__(self, player):
        self.spawn_random()
        self.player = player

    def render(self):
        surface = pygame.display.get_surface()
        pygame.draw.rect(
            surface, self.player.color, consts.cell(self.x, self.y)
        )

    def move(self, x, y):
        self.x, self.y = x, y

    def move_up(self):
        allowed = self.y > 0
        if allowed:
            self.y -= 1

    def move_down(self):
        allowed = self.y < consts.GRID_SIZE[1] - 1
        if allowed:
            self.y += 1

    def move_left(self):
        allowed = self.x > 0
        if allowed:
            self.x -= 1

    def move_right(self):
        allowed = self.x < consts.GRID_SIZE[0] - 1
        if allowed:
            self.x += 1

    def spawn_random(self):
        x, y = consts.GRID_SIZE
        self.x = random.randint(0, x)
        self.y = random.randint(0, y)
