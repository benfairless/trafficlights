from flask import url_for, jsonify
from . import api

from ..models import Check

@api.route('/checks/', methods=['GET'])
def get_checks():
    """Check object collection"""
    checks = Check.query.all()
    return jsonify({'checks': [check.to_json() for check in checks]})

@api.route('/checks/<int:id>/', methods=['GET'])
def get_check(id):
    """Check object resource"""
    check = Check.query.get_or_404(id)
    return jsonify(check.to_json())
