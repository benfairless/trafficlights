#!/usr/bin/env python
#
#
#
# ooo. .oo.  .oo.    .oooo.   ooo. .oo.    .oooo.    .oooooooo  .ooooo.      oo.ooooo.  oooo    ooo
# `888P"Y88bP"Y88b  `P  )88b  `888P"Y88b  `P  )88b  888' `88b  d88' `88b      888' `88b  `88.  .8'
#  888   888   888   .oP"888   888   888   .oP"888  888   888  888ooo888      888   888   `88..8'
#  888   888   888  d8(  888   888   888  d8(  888  `88bod8P'  888    .o .o.  888   888    `888'
# o888o o888o o888o `Y888""8o o888o o888o `Y888""8o `8oooooo.  `Y8bod8P' Y8P  888bod8P'     .8'
#                                                   d"     YD                 888       .o..P'
#                                                   "Y88888P'                o888o      `Y8P'

import os
from trafficlights import create_app
from flask_script import Manager, Shell, Command

# Initiate new application using the create_app function
app = create_app(os.getenv('TRAFFICLIGHT_CONFIG') or 'default')
manager = Manager(app)

def make_shell_context():
    return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))

# If you want to run administrative commands, or the debug server just run this
# script directly. If you want to access the WSGI application (for example with
# Gunicorn), just access manage:app directly.
if __name__ == '__main__':
    manager.run()
