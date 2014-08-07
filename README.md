[![Alt text](https://api.travis-ci.org/davide-ceretti/strategypy.svg?branch=master)](https://travis-ci.org/davide-ceretti/strategypy)
[![Alt text](http://coveralls.io/repos/davide-ceretti/strategypy/badge.png?branch=master)](https://coveralls.io/r/davide-ceretti/strategypy)

strategypy
----------

The idea is to provide a framework so that people can implement their own bot for a simple strategy game and compete versus each other. The project is currently in development (no alpha yet).

Most of the code not covered by unittests is pygame calls.

Installation
------------

* ```sudo apt-get install mercurial libfreetype6-dev python-dev python-numpy ffmpeg libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libsdl1.2-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev```
* ```pip install -r requirements.txt```

Usage
-----

* ```source scripts/run_tests```
* ```source scripts/run_example```

General usage is ```python strategypy/main.py <name_of_bot_one> <<name_of_bot_two> ...```

TODO / Improvements
-------------------

* API for Bots
* Security (Disable os, HTTP etc..)
* Anti-cheating (Isolate bots from what is not exposed by the API)
* Drop pygame for a JS FE (Game still played in Python)
* Numpy / Performance improvements
* Performance tracking
* Rework game rules and engine to make it more interesting
