#!/bin/sh

# Set-up keychain environnement
SHELL=/bin/sh
eval `keychain --noask --quiet --eval id_dsa`

# Set-up python environnement
export PYTHONIOENCODING=UTF-8
PYTHON3=/usr/local/bin/python3

# Run
${PYTHON3} -m anime_automove --config FULL_PATH_TO_CONF --learn
