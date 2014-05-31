import logging


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

    def __process_action__(self):
        """
        Interpret the message returned by action and execute it
        """
        action = self.action()
        if action not in self.__allowed_actions__:
            msg = 'Bot#%s executing not allowed action: %s' % (
                self.__unit__.player.pk, action)
            logging.warning(msg)
            return
        verb, arg = action.split(' ')
        self.__unit__.move(arg)
