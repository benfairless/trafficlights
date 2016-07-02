from flask import url_for, jsonify
from . import api

from ..models import Service

@api.route('/services/', methods=['GET'])
def get_services():
    """Service object collection"""
    services = Service.query.all()
    return jsonify({'services': [service.to_json() for service in services]})

@api.route('/services/<int:id>/', methods=['GET'])
def get_service(id):
    """Service object resource"""
    service = Service.query.get_or_404(id)
    return jsonify(service.to_json())

@api.route('/services/<int:id>/checks/', methods=['GET'])
def get_checks_for_service(id):
    """Check object collection for Service"""
    service = Service.query.get_or_404(id)
    return jsonify({'checks': [check.to_json() for check in service.checks]})
