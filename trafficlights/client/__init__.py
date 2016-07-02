import requests

class Client:

    def __init__(self, url):
        self.url = url

    def test(self):
        """Test the health endpoint of the webserver"""
        path = self.url + '/api/health'
        try:
            request = requests.get(path)
        except:
            return False

        if request.status_code == 200:
            return True
        else:
            return False

    def authenticate(self):
        return True

    def collect(self):
        """Retrieve checklist from server"""
        path = self.url + '/api/nodes/1/checks/'
        try:
            request = requests.get(path)
        except:
            return False
        return request.json()

    def submit(self):
        return True


client = Client('http://localhost:5000')
if client.test():
    print('Healthcheck looks good!')
    checklist = client.collect()
    print(checklist)
else:
    print('Healthcheck failed!')
