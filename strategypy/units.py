import pygame

from consts import cell


class Unit(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

    def render(self):
        red_color = pygame.Color(255, 0, 0)
        surface = pygame.display.get_surface()
        pygame.draw.rect(
            surface, red_color, cell(self.x, self.y)
        )

    def move(self, x, y):
        self.x, self.y = x, y
