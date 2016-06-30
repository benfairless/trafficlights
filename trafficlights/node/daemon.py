from worker import WorkProcessor
from time import sleep


def PutResults(data):
    print(data[0])
    return True


def Daemon():
    # Run forever, like all good daemons!
    # while True:
        tasklist = GetWorkList()
        results = WorkProcessor(tasklist)
        PutResults(results)
        # sleep(10)

Daemon()
