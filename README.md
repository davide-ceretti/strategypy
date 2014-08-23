[![Alt text](https://api.travis-ci.org/davide-ceretti/strategypy.svg?branch=master)](https://travis-ci.org/davide-ceretti/strategypy)
[![Alt text](http://coveralls.io/repos/davide-ceretti/strategypy/badge.png?branch=master)](https://coveralls.io/r/davide-ceretti/strategypy)

strategypy
----------

The idea is to create a framework so that people can implement their own bot for a simple strategy game and compete versus each other. The project is still in development, but if you checkout everything it is supposed to work just fine.

Pull requests are welcomed, expecially if you want to submit your own bot. Bear in mind the the BaseBot API is not final yet and it might change quite often.

Game rules
----------

Each player controls a set amount of cells in a grid. The behaviour of these cells is defined by a Bot that implements a specific interface; each cell of the player is represented by an instance of the Bot class.

The game ends when only one player has still cells alive in the grid.
A cell is killed if in the 9-cells subgrid centered on itself the number of the cells belonging to enemy players is more then the cells belonging to the owner of the cell.

Have a look at settings.py if you want to change some of the game basic settings.

Installation
------------

System dependencies:
* python2.7

* ```git clone https://github.com/davide-ceretti/strategypy.git```

Usage
-----

To run all the tests:
* ```pip install -r test-requirements.txt```
* ```./run_tests.sh```

To run an example game (output is json):
* ```./play.sh```

To run a game with simple console-based front-end:
* ```./play-console.sh```

To run a game with a PyGame front-end (Requires https://github.com/davide-ceretti/strategypy-pygame-client to be installed and it has python/system dependencies):
* ```./play-pygame.sh```

To run a game with a Javascript front-end on Firefox (Requires https://github.com/benqus/strategypy-ui and Firefox to be installed):
* ```./play-firefox.sh```


General usage:
* ```python strategypy/main.py <name_of_bot_one> <<name_of_bot_two> ...```

The result of the script is a JSON file that contains all the information necessary for any front-end to play it.

This can be either be saved on a file so that it can be loaded later by a FE:
* ```python strategypy/main.py killer prey prey```

or it can be piped it directly into a FE, for example:
* ```python strategypy/strategypy/main.py killer prey prey | python strategypy/simplefe.py```

See https://github.com/davide-ceretti/strategypy-pygame-client for a PyGame FE.
See https://github.com/benqus/strategypy-ui for a Javascript FE.


TODO / Improvements
-------------------

* API for Bots
* Security (Disable os, HTTP etc..)
* Anti-cheating (Isolate bots from what is not exposed by the API)
* Numpy / Performance improvements
* Performance tracking/acceptance on build
* Rework game rules and engine to make it more interesting
* More and better unit tests
* Package FE and their dpeendencies
