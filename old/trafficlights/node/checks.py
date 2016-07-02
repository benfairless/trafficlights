#
from queue import Queue
from threading import Thread

import requests
import json
from datetime import datetime

class Agent:

    def __init__(self, url):
        self.url = url
        self.token = '1234567890'

    def test(self):
        """
        Connects to server health check page to verify connection.
        STUB!
        """
        return True

    def worklist(self):
        """
        Collect worklist from server. Returns list of HealthCheck objects.
        ALPHA!
        """
        path = self.url + '/checks/' + self.token

        request = requests.get(path)
        response = json.loads(request.text)

        healthchecks = []
        for check in response['checks']:
            healthchecks.append(HealthCheck(check['url'],check['id']))
        return healthchecks

    def submit(self,completed):
        """
        Submit completed HealthCheck outputs to server.
        STUB!
        """
        path = self.url + '/results/' + self.token
        results = []
        for item in completed:
            results.append(item.result)
            print('Submitted %s' % item)
        data = { 'checks': results }
        payload = json.dumps(data)
        print(payload)
        headers = {'Content-Type': 'application/json'}
        r = requests.post(path, data = data, headers = headers)
        print(r.text)
        return True

    def _worker(self, input_queue, output_queue):
        """
        Queue based HealthCheck processor, taking HealthCheck objects from an
        in-memory queue, processing them, and then putting them onto an output
        queue. Designed to be used as a thread in self.process()
        """
        # Loop until there are no jobs remaining on the input queue.
        while not input_queue.empty():
            # Take a HealthCheck object off the input queue, process it and put
            # it on the output queue.
            check = input_queue.get()
            try:
                check.run()
                output_queue.put(check)
            except:
                pass
            else:
                # Clear check off the input queue if no error occured.
                input_queue.task_done()

    def process(self, workers=20):
        """
        Multi-threaded function for processing large numbers of HealthCheck
        objects simultaneously.
        """
        # Create in-memory queues for distributing work to multiple threads.
        input_queue  = Queue(0)
        output_queue = Queue(0)

        worklist = self.worklist()

        # Add all checks from worklist into input queue.
        for check in worklist:
            input_queue.put(check)

        # If there are less HealthCheck objects on the queue than workers
        # specified, scale down workers to match amount.
        if input_queue.qsize() < workers:
            workers = input_queue.qsize()

        # Initiate self._worker to process checks from input queue.
        threads = []
        for i in range(workers):
            thread = Thread(target=self._worker, args=(input_queue, output_queue))
            thread.start()
            threads.append(thread)

        # Block until all queue messages have been processed.
        input_queue.join()

        # Consume all messages from results queue and add to results list.
        results = []
        while not output_queue.empty():
            results.append(output_queue.get())
            output_queue.task_done()

        self.submit(results)
        return True


class HealthCheck:
    """
    HealthCheck object which carries out HTTP requests and records useful
    information about each request.
    """
    def  __init__(self, url, identifier):
        self.url      = url
        self.id       = identifier
        self.timeout  = 15
        self.metadata = None
        self.result   = None
        self.json     = None
        self.complete = False

    def __repr__(self):
        return '<HealthCheck %s>' % self.id

    def run(self):
        """
        Main run function which carries out healthcheck and populates fields
        with all appropriate information.
        """
        self.metadata = {}
        self.metadata['timestamp'] = datetime.utcnow()

        # Initiate request and populate fields with relevant information about
        # the request
        try:
            request = requests.get(self.url, timeout=self.timeout)
            self.metadata['code']    = request.status_code
            self.metadata['status']  = request.reason
            self.metadata['time']    = int(request.elapsed.microseconds / 1000)
            self.metadata['headers'] = dict(request.headers)
            self.metadata['content'] = request.text

        # In the event that an error occurs when attempting the request, a valid
        # HTTP status code will obviously not be returned.
        # Instead values will be returned which will aid in troubleshooting the
        # connection.
        except Exception as exception:
            self.metadata['code']    = 0
            self.metadata['status']  = type(exception).__name__
            self.metadata['time']    = self.timeout
            self.metadata['headers'] = {}
            self.metadata['content'] = exception.args

        self.complete = True
        self.generate()
        return True

    def generate(self):
        """
        Generates pretty result information, both as a dictionary at self.result
        and as JSON at self.json
        """
        result = {
            'id':       self.id,
            'url':      self.url,
            'metadata': self.metadata,
            'success':  self.success()
        }
        self.result = result

        # Before converting to JSON result['metadata']['timestamp'] will need
        # to be converted from a datetime object to a string.
        result['metadata']['timestamp'] = self.metadata['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        self.json = json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True)

    def success(self):
        """
        Produces boolean response as to whether the request was 'successful' or not.
        Success is determined by a 20X HTTP status code in the response.
        """
        # If HTTP status code is 2XX return True
        if (isinstance(self.metadata,dict) and 200 <= self.metadata['code'] < 300):
            return True
        else:
            return False
