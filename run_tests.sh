#!/usr/bin/env sh

export PYTHONPATH="src:$PYTHONPATH"
python2 -m pytest unittests $@
python3 -m pytest unittests $@
