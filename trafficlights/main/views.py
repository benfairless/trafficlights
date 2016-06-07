from flask import render_template, url_for
from . import main
from .. import db

# When using application blueprints you need to use the blueprint name in the
# function decorator.
@main.route('/', methods=['GET'])
def index():
    return 'Hello World'
