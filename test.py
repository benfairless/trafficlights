from trafficlights import db
from trafficlights.models import User, Node, Service, Check

def run():
    nodes = [
        'node-a',
        'node-b',
        'node-c',
        'node-d'
    ]
    services = [
        'TrafficLights',
        'service-2',
        'service-3'
    ]
    checks = [
        {
            'name': 'server',
            'check': 'https://trafficlights.herokuapp.com/api/health',
            'service': 1,
            'node': 1
        },
        {
            'name': 'local',
            'check': 'http://localhost:5000/api/health',
            'service': 1
        }
    ]
    users = [
        {
            'username': 'ben',
            'realname': 'Ben'
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

    # for user in users:
    #     u = User(user['username'], 'welcome1')
    #     u.realname = user['realname']
    #     db.session.add(u)
    # db.session.commit()

    return True
