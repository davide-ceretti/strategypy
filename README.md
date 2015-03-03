[![Alt text](https://api.travis-ci.org/davide-ceretti/strategypy.svg?branch=master)](https://travis-ci.org/davide-ceretti/strategypy)

strategypy
----------

A simple strategy game played by Python bots.

The project is still in development, but if you checkout everything and follow this README it is supposed to work just fine.

Pull requests are welcomed, expecially if you want to submit your own bot. Bear in mind the the BaseBot API is not final yet and it might change quite often.

Game rules
----------

Each player controls a set amount of cells in a grid. The behaviour of these cells is defined by a Bot that implements a specific interface; each cell of the player is represented by an instance of the Bot class.

The game ends when only one player has still cells alive in the grid.
A cell is killed if in the 9-cells subgrid centered on itself the number of the cells belonging to enemy players is more then the cells belonging to the owner of the cell.

Have a look at settings.py if you want to change some of the game basic settings.

Demo
----

Javascript Frontend: http://benqus.github.io/strategypy-ui/

Installation
------------

System dependencies: python2.7

* ```git clone https://github.com/davide-ceretti/strategypy.git```
* ```pip install -e .```

Quickstart
----------

To run an example game (output is json):
* ```./play.sh```

To run a game with simple console-based front-end:
* ```./play-simple.sh```

To run a game with a PyGame front-end (Requires https://github.com/davide-ceretti/strategypy-pygame-client and its dependencies):
* ```./play-pygame.sh```

To run a game with a Javascript front-end on Firefox (Requires https://github.com/benqus/strategypy-ui, its dependencies and Firefox to be installed):
* ```./play-firefox.sh```

To run a game with a console front-end (Requires https://github.com/mrfuxi/strategypy-consoleui):
* ```./play-console.sh```

General usage
-------------

* ```strategypy <name_of_bot_one> <<name_of_bot_two> ...```

The result of the script is a JSON file that contains all the information necessary for any front-end to play it.

The name of the bot must be a name of a python module in /bots/. It currently supports a URL of a web service that returns moves, but that is very experimental.

This JSON result can be saved on a file so that it can be loaded later by a FE:
* ```strategypy killer prey prey > example.json```

or it can be piped it directly into a FE, for example:
* ```strategypy killer prey prey | python strategypy/simplefe.py```

See https://github.com/davide-ceretti/strategypy-pygame-client for a PyGame FE.
See https://github.com/benqus/strategypy-ui for a Javascript FE.
See https://github.com/mrfuxi/strategypy-consoleui for a Console FE.

Tests
-----

To run all the tests:
* ```pip install tox```
* ```tox```


BOT API
-------

There are currently two ways to create a BOT.

The first and simplest one is to create a python file (e.g. mybot.py) in the bots directory. The python file must have a function called action.

The function "action" takes one argument, the context of the game and returns one of the five possible moves: 'move up', 'move left', 'move right', 'move down', None.

Example:
```
def action(ctx):
    return 'move down'
```

Then you can play a game by running:
```strategypy mybot <<name_of_bot_two> ...```

The second way (and experimental) to create a bot is by creating a web service that uses sockets. See https://github.com/davide-ceretti/strategypy-flask-bot-template as an example of a docker container running a flask service that uses sockets.

The game can then be played by running:
```strategypy <url_of_my_service> <<name_of_bot_two> ...```

For example (not expect it to work):
```strategypy strategypy-bot-example-davide-ceretti.delta.tutum.io:49158 static```

The context given to the action function represents the state of the game when action is required for one of your units. It is a dictionary with the following keys:

```
(int) player_pk
(int) pk
(bool) respawn
(int, int) grid_size
(int, int) position
(list) has_killed
(list) was_killed_by
(dict) current_data
```

TODO / Improvements
-------------------

* Better API for Bots
* Security in local mode
* Anti-cheating in local mode
* Numpy / Performance improvements
* Performance tracking/acceptance on build
* Rework game rules and engine to make it more interesting
* More and better unit tests
