import pygame

import consts
import bots
from players import Player


class Game(object):
    def __init__(self, *args):
        self.args = args
        self.init_screen()
        self.init_functions()
        self.init_players()

    def init_screen(self):
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60.0
        self.done = False

    def init_players(self):
        self.players = [
            Player(pk=i, action_func=function)
            for i, function in enumerate(self.functions)
        ]

    def init_functions(self):
        for arg in self.args:
            __import__('bots.{}'.format(arg))
        self.functions = [getattr(bots, arg).action for arg in self.args]

    @property
    def units(self):
        return [unit for player in self.players for unit in player.units]

    def event_loop(self):
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.done = True

    def update(self):
        for player in self.players:
            player.action()

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
