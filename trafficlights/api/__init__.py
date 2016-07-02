from flask import Blueprint

# Create new Flask Blueprint called api
api = Blueprint('api', __name__)

# Using relative paths to import submodules allows the easy duplication of blueprint modules.
from . import errors, nodes, services, checks, users, views
