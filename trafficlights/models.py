from flask import current_app, url_for
from flask_sqlalchemy import SQLAlchemy

from trafficlights import db

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    User accounts are used mainly to set up TrafficLights agents for now.
    """

    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80))
    password_hash = db.Column(db.String(156))
    displayname   = db.Column(db.String(80))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %s>' % self.id

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha512', salt_length=8)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        return {
            'id':          self.id,
            'username':    self.username,
            'displayname': self.realname
        }


class Node(db.Model):
    """
    Node objects are TrafficLights agents, responsible for running healthchecks
    and submitting results back to the TrafficLights server.
    """

    __tablename__ = 'nodes'
    id     = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(80))
    checks = db.relationship("Check", back_populates="node")

    def __init__(self, name):
        self.name  = name

    def __repr__(self):
        return '<Node %s>' % self.id

    def generate_auth_token(self, expiration):
        """Generate authentication token."""
        s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """Return Node object which matches authentication token"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            raise
            return None
        return Node.query.get(data['id'])

    def to_json(self):
        return {
            'id':     self.id,
            'name':   self.name,
            'url':    url_for('api.get_node', id=self.id, _external=True),
            'checks': url_for('api.get_checks_for_node', id=self.id, _external=True)
        }


class Service(db.Model):
    """
    Logical grouping of checks.
    """

    __tablename__ = 'services'
    id     = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(80))
    checks = db.relationship("Check", back_populates="service")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Service "%s">' % self.id

    def to_json(self):
        return {
            'id':     self.id,
            'name':   self.name,
            'url':    url_for('api.get_service', id=self.id, _external=True),
            'checks': url_for('api.get_checks_for_service', id=self.id, _external=True)
        }


class Check(db.Model):
    """
    Healthcheck configurations.
    """

    __tablename__ = 'checks'
    id    = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    service    = db.relationship("Service", back_populates="checks")
    node_id    = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    node       = db.relationship("Node", back_populates="checks")
    name  = db.Column(db.String(80))
    check = db.Column(db.String(120))
    # results    = db.relationship("Result", back_populates="check")

    def __init__(self, name, check, service):
        self.name       = name
        self.check      = check
        self.service_id = service

    def __repr__(self):
        return '<Check %s>' % self.id

    def to_json(self):
        return {
            'id':    self.id,
            'name':  self.name,
            'check': self.check,
            'url':   url_for('api.get_check', id=self.id, _external=True),
            'service': {
                'id':  self.service_id,
                'url': url_for('api.get_service', id=self.service_id, _external=True)
            }
        }
