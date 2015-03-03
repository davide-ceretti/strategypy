import logging
import json

from websocket import create_connection

import bots


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
            None,
        ]

        self.__static_data__ = ctx

    def action(self, ctx):
        """
        To be implented in the super class.
        It is supposed to return one of the action defined
        in __allowed_actions__.
        ctx contains all the available data in the game:
            (int) player_pk
            (int) pk
            (bool) respawn
            (int, int) grid_size
            (int, int) position
            (list) has_killed
            (list) was_killed_by
            (dict) current_data

        """

        raise NotImplementedError

    def __process_action__(self, ctx):
        """
        Interpret the message returned by action and execute it
        """
        action = self.action(ctx)

        if action not in self.__allowed_actions__:
            msg = 'Bot#%s executing not allowed action: %s' % (
                ctx['player_pk'], action)
            logging.warning(msg)
            return

        if action is None:
            return

        verb, arg = action.split(' ')

        return arg


def make_socket_bot(arg):
    WS = create_connection("ws://{}".format(arg))

    class SocketBot(BaseBot):
        url = arg
        name = arg
        ws = WS

        def action(self, ctx):
            self.ws.send(json.dumps(ctx))
            result = self.ws.recv()
            return result

    return SocketBot


def make_local_bot(arg):
    __import__('strategypy.bots.{}'.format(arg))
    bot_module = getattr(bots, arg)

    class LocalBot(BaseBot):
        name = bot_module.__name__.split('.')[-1]

        def action(self, ctx):
            return bot_module.action(ctx)

    return LocalBot
