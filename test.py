from trafficlights import db
from trafficlights.models import Node, Service, Check

def run():
    nodes = [
        'node-a',
        'node-b',
        'node-c',
        'node-d'
    ]
    services = [
        'service-1',
        'service-2',
        'service-3'
    ]
    checks = [
        {
            'name': 'check-a',
            'check': 'http://google.com/',
            'service': 1,
            'node': 1
        },
        {
            'name': 'check-b',
            'check': 'http://github.com/',
            'service': 1
        }
    ]

    db.drop_all()
    db.create_all()

    for node in nodes:
        n = Node(node)
        db.session.add(n)

    for service in services:
        s = Service(service)
        db.session.add(s)

    db.session.commit()

    for check in checks:
        c = Check(check['name'], check['check'], check['service'])
        db.session.add(c)
    db.session.commit()

    s = Check.query.first()
    s.node_id = 1
    db.session.add(s)
    db.session.commit()

    return True
