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
        self.__previous_position__ = self.position

    def action(self):
        """
        To be implented in the super class.
        It is supposed to return one of the action defined
        in __allowed_actions__.
        """
        raise NotImplementedError

    @property
    def position(self):
        """
        The position of the unit in the grid
        """
        return self.__unit__.current_cell

    @property
    def previous_position(self):
        """
        The position of the unit before the last action.
        """
        return self.__previous_position__

    def __process_action__(self):
        """
        Interpret the message returned by action and execute it
        """
        pos = self.position
        action = self.action()
        if action not in self.__allowed_actions__:
            if action is not None:
                msg = 'Bot#%s executing not allowed action: %s' % (
                    self.__unit__.player.pk, action)
                logging.warning(msg)
            return
        verb, arg = action.split(' ')
        self.__unit__.move(arg)
        self.__previous_position__ = pos

    @property
    def grid_size(self):
        """
        Return the size of the grid (X, Y)
        """
        return settings.GRID_SIZE
