from checks import Agent, HealthCheck
from time import sleep

client = Agent('http://localhost:5000')

if client.test():
    while True:
        client.process()
        sleep(10)
