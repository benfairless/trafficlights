import requests
from datetime import datetime

# HealthCheck object which carries out HTTP requests and records useful
# information about each request.
class  HealthCheck:

    def __init__(self, url):
        self.url       = url
        self.timeout   = 15
        self.metadata  = None
        self.headers   = None
        self.content   = None
        self.run()

    # Main run function which carries out healthcheck and populates fields with
    # all appropriate information.
    def run(self):
        self.metadata = {}
        self.metadata['timestamp'] = datetime.utcnow()

        # Initiate request and populate fields with relevant information about
        # the request.
        try:
            request = requests.get(self.url, timeout=self.timeout)
            self.metadata['code']   = request.status_code
            self.metadata['status'] = request.reason
            self.metadata['time']   = int(request.elapsed.microseconds / 1000)
            self.headers            = request.headers
            self.content            = request.text

        # In the event that an error occurs when attempting the request, a valid
        # HTTP status code will obviously not be returned.
        # Instead values will be returned which will aid in troubleshooting the
        # connection.
        except Exception as exception:
            self.metadata['code']   = 0
            self.metadata['status'] = type(exception).__name__
            self.metadata['time']   = self.timeout # Need to check if these values are represented in milliseconds.
            self.headers            = {}
            self.content            = exception.args

    # Produces boolean response as to whether the request was 'successful' or
    # not. Success is determined by a 20X HTTP status code in the response.
    def success(self):

        # If HTTP status code is 2XX return True
        if (isinstance(self.metadata,dict) and 200 <= self.metadata['code'] < 300):
            return True
        else:
            return False

    # Returns dictionary of all information collected from the request.
    def results(self):
        return {
            'url':      self.url,
            'metadata': self.metadata,
            'headers':  self.headers,
            'content':  self.content
        }
