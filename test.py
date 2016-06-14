from trafficlights.models import Service, Check, Node
from trafficlights import db, create_app

def run_load():

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
