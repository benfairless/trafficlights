from flask import render_template, url_for, request
from . import main

@main.route('/', methods=['GET'])
def index():
    return 'Hello World'
