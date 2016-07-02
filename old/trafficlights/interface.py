from .models import Node, Check, Result, Service
from . import db

from datetime import datetime

def generateChecklist(node):
    """
    Return list of checks for a specific node, based on the node's id
    """
    results = []
    checks = Check.query.filter_by(node_id=node)

    for check in checks:
        results.append({'id': check.id, 'url': check.url})

    return results

def identifyNode(token):
    """
    Identify a node by it's token.
    """
    node = Node.query.filter_by(token=token).first()
    return node

def storeResults(resultlist,node):
    for result in resultlist:
        # Convert timestamp into datetime object.
        db.session.add(Result(node,result))
    db.session.commit()


###############################################################################

def populateTest():
    services = [
        'alpha',
        'beta'
    ]

    nodes = [
        'one',
        'two'
    ]

    alpha = [
        { 'name': 'google', 'url': 'http://google.com', 'service': 1, 'node': 1 },
        { 'name': 'github', 'url': 'http://github.com', 'service': 2, 'node': 2 }
    ]

    print('Adding services')
    for service in services:
        print('Adding %s' % service)
        s = Service(service)
        db.session.add(s)

    for node in nodes:
        print('Adding %s' % node)
        s = Node(node)
        db.session.add(s)

    db.session.commit()

    print ('Adding checks')
    for item in alpha:
        print(item)
        s = Check(item['name'],item['url'],service=1,node=1)
        db.session.add(s)

    db.session.commit()
