from flask_sqlalchemy import SQLAlchemy
from trafficlights import db

from datetime import datetime


class User(db.Model):
    """
    User account details.
    """

    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(48))
    password_hash = db.Column(db.String(64))

    def __init__(self, username, password_hash):
        self.username      = username
        self.password_hash = password_hash

    def __repr__(self):
        return '<User %s>' % self.username

class Node(db.Model):
    __tablename__ = 'nodes'
    id      = db.Column(db.Integer, primary_key=True)
    checks  = db.relationship("Check", back_populates="node")
    results = db.relationship("Result", back_populates="node")
    name    = db.Column(db.String(80))
    token   = db.Column(db.String(80))

    def __init__(self, name):
        self.name  = name
        self.token = '1234567890'


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
        return '<Service "%s">' % self.name


class Check(db.Model):
    """
    Healthcheck configurations.
    """

    __tablename__ = 'checks'
    id         = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    node_id    = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    service    = db.relationship("Service", back_populates="checks")
    node       = db.relationship("Node", back_populates="checks")
    results    = db.relationship("Result", back_populates="check")
    name = db.Column(db.String(80))
    url  = db.Column(db.String(80))

    def __init__(self, name, url, service, node):
        self.name       = name
        self.url        = url
        self.service_id = service
        self.node_id    = node

    def __repr__(self):
        return '<Check "%s - %s">' % (self.service.name, self.name)

class Result(db.Model):
    """
    Results from Healthchecks.
    """
    # So I'm really not sure how best to manage the result objects. For now
    # it seems best to just create them using the entire dictionary, populating
    # the relevant fields...
    __tablename__ = 'results'
    id       = db.Column(db.Integer, primary_key=True)
    check_id = db.Column(db.Integer, db.ForeignKey('checks.id'))
    check    = db.relationship("Check", back_populates="results")
    node_id  = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    node     = db.relationship("Node", back_populates="results")

    code      = db.Column(db.Integer)
    status    = db.Column(db.Text)
    time      = db.Column(db.Integer)
    headers   = db.Column(db.Text)
    content   = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    success   = db.Column(db.Boolean)
    url       = db.Column(db.Text)

    def __init__(self, node, data):
        self.node_id  = node
        self.check_id = data['id']

        self.code      = data['metadata']['code']
        self.status    = data['metadata']['status']
        self.time      = data['metadata']['time']
        self.headers   = str(data['metadata']['headers'])
        self.content   = data['metadata']['content']
        self.timestamp = datetime.strptime(data['metadata']['timestamp'], '%Y-%m-%d %H:%M:%S')
        self.success   = data['success']
        self.url       = data['url']

    def __repr__(self):
        return '<Result %i>' % id
#
# Object for storing healthchecks. Requires a name, and a URL to check.
# class Check(db.Model):
#
#
#     id   = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120))
#     url   = db.Column(db.String(120))
#
#     service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
#
#     def __init__(self,name,url,service):
#         self.name = name
#         self.url  = url
#         self.service_id = service
#
#
#
#     __tablename__ = 'results'
#
#     id        = db.Column(db.Integer, primary_key=True)
#     check_id  = db.Column(db.Integer, db.ForeignKey('checks.id')) # ID of appropriate check.
#     timestamp = db.Column(db.DateTime)
#     code      = db.Column(db.Text)
#     status    = db.Column(db.Text)
#     time      = db.Column(db.Text)
#     content   = db.Column(db.Text)
#     headers   = db.Column(db.Text)
#
#     def __init__(self,result):
#         self.check_id  = result['id']
#         self.timestamp = result['timestamp']
#         self.code      = result['metadata']['code']
#         self.status    = result['metadata']['status']
#         self.time      = result['metadata']['time']
#         self.content   = result['content']
#         self.headers   = result['headers']
#
#     def __repr__(self):
#         return '<Result %i>' % self.id
