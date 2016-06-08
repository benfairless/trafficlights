from worker import WorkProcessor
from time import sleep

def GetWorkList():
    return [
        {
            'id': 5000,
            'url': 'http://google.com/'
        },
        {
            'id': 5001,
            'url': 'http://github.com/'
        },
        {
            'id': 5002,
            'url': 'http://gov.uk/'
        }
    ]

def PutResults(data):
    print(data)
    return True


def Daemon():
    # Run forever, like all good daemons!
    while True:
        tasklist = GetWorkList()
        results = WorkProcessor(tasklist)
        PutResults(results)
        sleep(10)

Daemon()
