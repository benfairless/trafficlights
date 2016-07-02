from flask import render_template, url_for, request, jsonify
from . import api

from ..models import Node, Service, Check

@api.route('/', methods=['GET'])
def index():
    """Index page"""
    routes = [
        {
            'name':        index.__name__,
            'url':         url_for('api.index', _external=True),
            'description': index.__doc__
        },
        {
            'name':        health.__name__,
            'url':         url_for('api.health', _external=True),
            'description': health.__doc__
        }
    ]
    return jsonify({'routes': routes})

@api.route('/health', methods=['GET'])
def health():
    """Healthcheck endpoint"""
    return jsonify({'status': 'ok'})

@api.route('/token', methods=['GET'])
def get_token():
    """STUB token generation"""
    node = Node.query.first()
    expiration = 300
    token = node.generate_auth_token(expiration=expiration)
    return jsonify({'token': token.decode('utf-8'), 'expiration': expiration})
