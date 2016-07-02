from flask import g, jsonify
from flask.ext.httpauth import HTTPBasicAuth

from ..models import Node
from . import api
from .errors import unauthorized, forbidden

# Initialise authentication object
auth = HTTPBasicAuth()

@auth.verify_password
def verify_token(token):
    if token == '':
        return False
    g.current_user = Node.verify_auth_token(token)
    g.token_used = True
    return g.current_user
