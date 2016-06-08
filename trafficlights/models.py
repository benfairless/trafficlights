from flask_sqlalchemy import SQLAlchemy
from trafficlights import db


# Object for storing healthchecks. Requires a name, and a URL to check.
class Check(db.Model):

    __tablename__ = 'checks'

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    url  = db.Column(db.String(120))

    def __init__(self,name,url):
        self.name = name
        self.url  = url

    def __repr__(self):
        return '<Check %s>' % self.name


# Object for managing 'Services', which are logical groups of checks.
class Service(db.Model):

    __tablename__ = 'services'

    id     = db.Column(db.Integer, primary_key=True)
    name   = db.Column(db.String(80), unique=True)
    # checks = db.relationship('Check', backref='service', lazy='dynamic')

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Service %r>' % self.name


class Result(db.Model):

    __tablename__ = 'results'

    id        = db.Column(db.Integer, primary_key=True)
    check_id  = db.Column(db.Integer, db.ForeignKey('checks.id')) # ID of appropriate check.
    timestamp = db.Column(db.DateTime)
    code      = db.Column(db.Text)
    status    = db.Column(db.Text)
    time      = db.Column(db.Text)
    content   = db.Column(db.Text)
    headers   = db.Column(db.Text)

    def __init__(self,result):
        self.check_id  = result['id']
        self.timestamp = result['timestamp']
        self.code      = result['metadata']['code']
        self.status    = result['metadata']['status']
        self.time      = result['metadata']['time']
        self.content   = result['content']
        self.headers   = result['headers']

    def __repr__(self):
        return '<Result %i>' % self.id
