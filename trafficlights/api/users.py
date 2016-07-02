from flask import url_for, jsonify
from . import api

from ..models import User


@api.route('/users/', methods=['GET'])
def get_users():
    """User object collection"""
    users = User.query.all()
    return jsonify({'users': [user.to_json() for user in users]})

@api.route('/users/<int:id>/', methods=['GET'])
def get_user(id):
    """User object resource"""
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())
