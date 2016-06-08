from flask import Blueprint

# Create a new Flask blueprint called 'main'.
main = Blueprint('main', __name__)

# Using relative paths to import submodules allows the easy duplication of blueprint modules.
from . import errors, views