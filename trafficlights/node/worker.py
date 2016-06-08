from threading import Thread
from queue import Queue
from checks import HealthCheck


# Queue based HealthCheck worker, taking tasks from an in-memory queue, processing them, and
# putting results into another queue. Designed to be used as a worker thread in a
# multi-threaded function.
def QueueWorker(task_queue,result_queue):
    # Loop until there is no work left on the task queue.
    while not task_queue.empty():
        # Take a task off the task queue, process it, put the response on the output queue.
        task = task_queue.get()
        try:
            result       = HealthCheck(task['url']).results()
            result['id'] = task['id'] # Pass through the task ID to include with the results.
            result_queue.put(result)  # Add result onto result queue.
        except:
            pass
        else:
            task_queue.task_done()    # Clear task off task queue.


# Multi-threaded function for processing large numbers of HealthChecks simultaneously.
# When provided with a list of HealthCheck tasks it will output a list of results.
def WorkProcessor(tasklist, workers=20):
    # Create in-memory queues for distributing work to multiple threads.
    task_queue   = Queue(0)
    result_queue = Queue(0)

    # Add all tasks from task list into the task queue.
    for task in tasklist:
        task_queue.put(task)

    # Initiate QueueWorkers to process tasks from task queue.
    threads = []
    for i in range(workers):
        thread = Thread(target=QueueWorker,args=(task_queue, result_queue))
        thread.start()
        threads.append(thread)

    # Block until all queue messages have been processed.
    task_queue.join()

    # Consume all messages from results queue and add to results list.
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
        result_queue.task_done()

    return results
