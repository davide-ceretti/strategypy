import logging

import settings


class BaseBot(object):
    """
    Base class for all the bots.
    """
    def __init__(self, unit):
        self.__unit__ = unit
        self.__allowed_actions__ = [
            'move up',
            'move left',
            'move right',
            'move down',
        ]

    def action(self):
        """
        To be implented in the super class.
        It is supposed to return one of the action defined
        in __allowed_actions__.
        """
        raise NotImplementedError

    @property
    def has_killed(self, unit):
        return self.__unit__.has_killed

    @property
    def was_killed_by(self, units):
        return self.__unit__.was_killed_by

    @property
    def respawned(self):
        return self.__unit__.respawned

    @property
    def data(self):
        return self.__unit__.player.game.data[:]

    @property
    def current_data(self):
        return self.__unit__.player.game.current_data()

    @property
    def pk(self):
        return self.__unit__.pk

    @property
    def player_pk(self):
        return self.__unit__.player.pk

    @property
    def position(self):
        """
        The position of the unit in the grid
        """
        return self.__unit__.current_cell

    def __process_action__(self):
        """
        Interpret the message returned by action and execute it
        """
        action = self.action()
        if action not in self.__allowed_actions__:
            if action is not None:
                msg = 'Bot#%s executing not allowed action: %s' % (
                    self.__unit__.player.pk, action)
                logging.warning(msg)
            return
        verb, arg = action.split(' ')
        self.__unit__.move(arg)

    @property
    def grid_size(self):
        """
        Return the size of the grid (X, Y)
        """
        return settings.GRID_SIZE
