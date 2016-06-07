#!/usr/bin/env bash
#
#                        .                                       oooo
#                      .o8                                       `888
#  .oooo.o  .ooooo.  .o888oo oooo  oooo  oo.ooooo.       .oooo.o  888 .oo.
# d88(  "8 d88' `88b   888   `888  `888   888' `88b     d88(  "8  888P"Y88b
# `"Y88b.  888ooo888   888    888   888   888   888     `"Y88b.   888   888
# o.  )88b 888    .o   888 .  888   888   888   888 .o. o.  )88b  888   888
# 8""888P' `Y8bod8P'   "888"  `V88V"V8P'  888bod8P' Y8P 8""888P' o888o o888o
#                                         888
#                                        o888o
#
# Sets up a Python virtual environment, installs packages defined in
# ./requirements.txt and starts a new shell inside the virtual environment

DIR=$(dirname $0)
VENV="${DIR}/venv"

if [[ ! -d $VENV ]]; then
    echo "Creating virtualenv at ${VENV}"
    pyvenv "${VENV}"
    [[ $? != '0' ]] && echo 'Errors occured during the setup process' && exit 1
else
    echo "Using existing virtualenv at ${VENV}"
fi

$VENV/bin/pip install -r "${DIR}/requirements.txt" --upgrade

source $VENV/bin/activate
bash
