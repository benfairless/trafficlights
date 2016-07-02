from flask import url_for, jsonify
from . import api

from ..models import Node

@api.route('/nodes/', methods=['GET'])
def get_nodes():
    """Node object collection"""
    nodes = Node.query.all()
    return jsonify({'nodes': [node.to_json() for node in nodes]})

@api.route('/nodes/<int:id>/', methods=['GET'])
def get_node(id):
    """Node object resource"""
    node = Node.query.get_or_404(id)
    return jsonify(node.to_json())

@api.route('/nodes/<int:id>/checks/', methods=['GET'])
def get_checks_for_node(id):
    """Check object collection for Node"""
    node = Node.query.get_or_404(id)
    return jsonify({'checks': [check.to_json() for check in node.checks]})
