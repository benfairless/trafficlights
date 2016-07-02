from flask import render_template, url_for, request
from . import api

from .. import interface

@api.route('/', methods=['GET'])
def index():
    return interface.test()

@api.route('/nodes/<node>', methods=['GET'])
def nodes(node):
    """ Return node object resource """
    return node

@api.route('/services/<service>', methods=['GET'])
def services(service):
    """ Return service object resource """
    return service

@api.route('/services/<service>/checks', methods=['GET'])
def services_checks(service):
    """ Return check object collection for service """
    return 'SERVICE results'

@api.route('/checks/<check>', methods=['GET'])
def checks(check):
    """ Return check object resource """
    return check

@api.route('/checks/<check>/results', methods=['GET'])
def checks_results(check):
    """ Return results object collection for check """
    return 'CHECK results'

@api.route('/results/<result>', methods=['GET'])
def results(result):
    """ Return result object resource """
    return result
