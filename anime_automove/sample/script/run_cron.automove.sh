#!/bin/sh

# Set-up keychain environnement
SHELL=/bin/sh
eval `keychain --noask --quiet --eval id_dsa`

# Set-up python environnement
export PYTHONIOENCODING=UTF-8
PYTHON27=/usr/local/bin/python2.7

# Run
${PYTHON27} -m anime_automove --config FULL_PATH_TO_CONF --execute
