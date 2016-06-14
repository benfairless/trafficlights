from flask_sqlalchemy import SQLAlchemy
from trafficlights import db


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
#     results    = db.relationship("Result", back_populates="check")
    name = db.Column(db.String(80))
    url  = db.Column(db.String(80))

    def __init__(self, name, url, service, node):
        self.name       = name
        self.url        = url
        self.service_id = service
        self.node_id    = node

    def __repr__(self):
        return '<Check "%s - %s">' % (self.service.name, self.name)
#
#
# class Result(db.Model):
#     """
#     Results from Healthchecks.
#     """
#
#     __tablename__ = 'results'
#     id       = db.Column(db.Integer, primary_key=True)
#     check_id = db.Column(db.Integer, db.ForeignKey('checks.id'))
#     check    = db.relationship("Check", back_populates="checks")
#     node_id  = db.Column(db.Integer, db.ForeignKey('nodes.id'))
#     node     = db.relationship("Node", back_populates="results")
#
#     def __repr__(self):
#         return '<Result %i>' % id
#
#
class Node(db.Model):
    __tablename__ = 'nodes'
    id     = db.Column(db.Integer, primary_key=True)
    checks = db.relationship("Check", back_populates="node")
    # results = db.relationship("Check", back_populates="node")
    name   = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name
#
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
