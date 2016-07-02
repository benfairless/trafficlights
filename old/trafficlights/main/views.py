from flask import render_template, url_for, request
from . import main
from .. import db

from ..interface import generateChecklist, identifyNode, storeResults, populateTest

import json

# When using application blueprints you need to use the blueprint name in the
# function decorator.
@main.route('/', methods=['GET'])
def index():
    return 'Hello World'

@main.route('/health', methods=['GET'])
def healtcheck():
    return 'OK'

@main.route('/checks/<token>', methods=['GET'])
def checks(token):
    node = identifyNode(token)
    response = {
        'checks': generateChecklist(node.id)
    }
    return json.dumps(response)

@main.route('/results/<token>', methods=['POST'])
def results(token):
    node = identifyNode(token)
    checks = request.json
    # storeResults(checks['checks'], node)
    return token

@main.route('/show', methods=['POST'])
def show():
    d = request.json
    print(d)
    return str(d)

@main.route('/test', methods=['GET'])
def test():

    populateTest()

    data = [{
        'success': True,
        'url': 'http://google.com',
        'id': 1,
        'metadata': {
            'status': 'OK',
            'timestamp': '2016-07-01 20:28:18',
            'content': 'TEST',
            'time': 521,
            'headers': {
              'Content-Length': '4500',
              'Cache-Control': 'private, max-age=0',
              'Expires': '-1',
              'X-XSS-Protection': '1; mode=block',
              'Server': 'gws',
              'Date': 'Fri, 01 Jul 2016 20:28:19 GMT',
              'Content-Encoding': 'gzip',
              'Content-Type': 'text/html; charset=ISO-8859-1',
              'X-Frame-Options': 'SAMEORIGIN'
            },
            'code': 200
        }
    }]
    storeResults(data,1)
    return 'Good'
