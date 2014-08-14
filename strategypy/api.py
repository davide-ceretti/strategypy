import logging

import settings


class BaseBot(object):
    """
    Base class for all the bots.
    """
    def __init__(self, ctx):
        self.__allowed_actions__ = [
            'move up',
            'move left',
            'move right',
            'move down',
        ]

        self.player_pk = ctx['player_pk']
        self.pk = ctx['pk']
        self.respawn = ctx['respawn']
        self.grid_size = ctx['grid_size']

        self.current_data = None
        self.has_killed = None
        self.was_killed_by = None
        self.position = None
        
    def action(self, ctx):
        """
        To be implented in the super class.
        It is supposed to return one of the action defined
        in __allowed_actions__.
        """

        raise NotImplementedError


    def __process_action__(self, ctx):
        """
        Interpret the message returned by action and execute it
        """
        self.current_data = ctx['current_data']
        self.has_killed = ctx['has_killed']
        self.was_killed_by = ctx['was_killed_by']
        self.position = ctx['position']
        
        action = self.action(ctx)

        if action not in self.__allowed_actions__:
            if action is not None:
                msg = 'Bot#%s executing not allowed action: %s' % (
                    self.__unit__.player.pk, action)
                logging.warning(msg)
            return

        verb, arg = action.split(' ')
        
        return arg
