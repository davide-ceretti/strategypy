[![Alt text](https://api.travis-ci.org/davide-ceretti/strategypy.svg?branch=master)](https://travis-ci.org/davide-ceretti/strategypy)
[![Alt text](http://coveralls.io/repos/davide-ceretti/strategypy/badge.png?branch=master)](https://coveralls.io/r/davide-ceretti/strategypy)

strategypy
----------

The idea is to provide a framework so that people can implement their own bot for a simple strategy game and compete versus each other. The project is currently in development (no alpha yet).

Installation
------------

* ```pip install -r requirements.txt```

Usage
-----

* ```./run_tests```
* ```./run_example```

General usage is ```python strategypy/main.py <name_of_bot_one> <<name_of_bot_two> ...```

The result of the script is a JSON file that contains all the information necessary for any front-end to play it.

You might want to pipe it to a FE, for example:

python strategypy/main.py move_up move_down move_left move_right | python strategypy/simplefe.py


TODO / Improvements
-------------------

* API for Bots
* Security (Disable os, HTTP etc..)
* Anti-cheating (Isolate bots from what is not exposed by the API)
* Numpy / Performance improvements
* Performance tracking
* Rework game rules and engine to make it more interesting
* Build JS front-end
