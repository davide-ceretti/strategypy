import pygame

import settings
import bots
from core.players import Player


class Game(object):
    def __init__(self, *args):
        self.args = args
        self.occupied_cells = []
        self.init_screen()
        self.init_functions()
        self.init_players()
        self.done = False

    def set_occupied_cells(self):
        """
        Update the list of the cells currently occupied by units
        """
        self.occupied_cells = [(unit.x, unit.y) for unit in self.units]

    def init_screen(self):
        """
        Initialize screen
        """
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = settings.FPS

    def init_players(self):
        """
        Create Players according to the loaded functions
        """
        self.players = [
            Player(pk=i, action_func=function, game=self)
            for i, function in enumerate(self.functions)
        ]

    def init_functions(self):
        """
        Create bot action functions by getting the name of the
        package/module from the args
        """
        for arg in self.args:
            __import__('bots.{}'.format(arg))
        self.functions = [self._get_action(arg) for arg in self.args]

    def _get_action(self, module_path):
        """
        Take the name of the module (i.e. tests.test_one or test_one)
        and returns the action function as defined in the module
        """
        return getattr(bots, module_path).action

    @property
    def units(self):
        """
        All the units in the Game
        """
        return [unit for player in self.players for unit in player.units]

    def event_loop(self):
        """
        Fetch for events
        """
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.done = True

    def update(self):
        """
        Fetch all unit positions and action units
        """
        self.set_occupied_cells()
        for player in self.players:
            player.action()

    def draw(self):
        """
        Main drawing function called in the infinite loop
        """
        self.screen.fill(settings.BG_COLOR)
        for unit in self.units:
            unit.render()
        self.draw_grid()

    def draw_grid(self):
        """
        Draw a grid according to the game settings
        """
        X, Y = settings.SCREEN_SIZE
        gap_x, gap_y = settings.UNIT_SIZE
        for i in xrange(0, X+1, gap_x):
            pygame.draw.line(
                self.screen,
                settings.GRID_COLOR,
                (i, 0),
                (i, Y),
                1,
            )
        for i in xrange(0, Y+1, gap_y):
            pygame.draw.line(
                self.screen,
                settings.GRID_COLOR,
                (0, i),
                (X, i),
                1,
            )

    def display_fps(self):
        """
        Show the program's FPS in the window handle
        """
        fps = self.clock.get_fps()
        caption = "{} - FPS: {:.2f}".format(settings.CAPTION, fps)
        pygame.display.set_caption(caption)

    def main_loop(self):
        """
        The main loop of the game, can be interrupted by events
        """
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.fps)
            self.display_fps()
