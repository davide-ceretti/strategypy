import pygame

import consts
from units import Unit


class Game(object):
    def __init__(self):
        self.init_screen()
        self.init_units()

    def init_screen(self):
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60.0
        self.done = False

    def init_units(self):
        self.units = [Unit(0, 0) for _ in xrange(0, 20)]

    def event_loop(self):
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.done = True

    def update(self):
        from random import randint
        x, y = consts.GRID_SIZE
        for unit in self.units:
            unit.move(randint(0, x), randint(0, y))

    def draw(self):
        self.screen.fill((0, 0, 0))
        for unit in self.units:
            unit.render()
        self.draw_grid()

    def draw_grid(self):
        X, Y = consts.SCREEN_SIZE
        gap_x, gap_y = consts.UNIT_SIZE
        for i in xrange(0, X+1, gap_x):
            pygame.draw.line(
                self.screen,
                consts.GRID_COLOR,
                (i, 0),
                (i, Y),
                1,
            )
        for i in xrange(0, Y+1, gap_y):
            pygame.draw.line(
                self.screen,
                consts.GRID_COLOR,
                (0, i),
                (X, i),
                1,
            )

    def display_fps(self):
        """Show the program's FPS in the window handle."""
        fps = self.clock.get_fps()
        caption = "{} - FPS: {:.2f}".format(consts.CAPTION, fps)
        pygame.display.set_caption(caption)

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.fps)
            self.display_fps()
