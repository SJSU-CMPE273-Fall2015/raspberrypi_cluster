__author__ = 'saurabh'
import time
from .exceptions import *


# If pubsub model is implemented, this will be required
#
# class ClusterIdentifier(object):
#     def __init__(self, ip, port):
#         self.ip = ip;
#         self.port = port;


class TaskState(object):
    PENDING = 'PENDING'
    STARTED = 'STARTED'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'


class PRIORITY(object):
    LOW_PRIORITY = 3
    MED_PRIORITY = 2
    HIGH_PRIORITY = 1
    EMERGENCY = 0


class SimpleQueueTask(object):
    def __init__(self, task_id, data, priority=3):
        self.task_id = task_id
        self.status = TaskState.PENDING
        self.time = time.time()
        self.data = data
        self.priority = priority

    def __str__(self, *args, **kwargs):
        return str(self.task_id) + ":" + str(self.time) + ":" + self.status + ":" + str(self.priority) + ":" + str(
            self.data)

    def __repr__(self):
        return self.__str__()


class SimplePriorityQueue(object):
    MAX_PRIORITY = PRIORITY.LOW_PRIORITY

    def __init__(self, topic, size):
        self.heap = []
        self.topic = topic
        self.size = size
        self.healthCheckUp()

    def has_more(self):
        return len(self.heap) > 0

    def is_full(self):
        return len(self.heap) == self.size

    def size(self):
        return len(self.heap)

    def enqueue(self, task=SimpleQueueTask):
        if self.is_full():
            return False
        self.heap.append(task)
        return True

    def dequeue(self):
        if not self.has_more():
            return None

        highest_priority = self.MAX_PRIORITY

        iter = 0
        index = 0

        for task in self.heap:
            if task.priority < highest_priority:
                highest_priority = task.priority
                index = iter
            iter += 1
        return self.heap.pop(index)

    def __str__(self):
        return str(self.heap)

    def __repr__(self):
        return self.__str__()

    def healthCheckUp(self):
        """
        Method to check health of the queue. If Task is timed out, removes it and put it in failure queue.
        Runs periodically.

        """
        # TODO This thread becomes zombie. Correct implementation needed.
        print("Checking Queue Health..." + str(self.heap) + self.topic)
        import time
        for task in self.heap:
            if time.time() - task.time >= 20:
                task.status = TaskState.FAILURE
                manager.failure_queue.enqueue(task)
                self.heap.remove(task)
                print("Removed task:", task)
        import threading
        threading.Timer(3.0, self.healthCheckUp).start()


class QueueManager(object):
    def __init__(self):
        """
        Initializes queue dictionary. Adds two must present queues for success and failure.

        """
        self.queues = {'success': SimplePriorityQueue('success', 500), 'failure': SimplePriorityQueue('failure', 500)}
        self.success_queue = self.queues['success']
        self.failure_queue = self.queues['failure']

    def getQueue(self, topic):
        if topic not in self.queues:
            return None
        return self.queues.get(topic)

    def createQueue(self, topic, size):
        if topic in self.queues:
            return False
        queue = SimplePriorityQueue(topic, size)
        self.queues[topic] = queue
        return True

    def enqueue(self, topic, task):
        queue = self.getQueue(topic)
        if queue is None:
            return QueueNotPresentException
        return queue.enqueue(task)

    def addToSuccessQueue(self, task):
        self.success_queue.enqueue(task)

    def checkStatus(self, topic, task_id):
        """
        Method to check task status.

        Method first looks into queue with the specified topic. If not available, searches in "success" queue. If not
        searches in "failure" queue. If not present in all these queues, that means task is lost and should be a
        failure.

        :param topic: Topic of the channel in which task was enqueued
        :param task_id: Id of the task
        :rtype : TaskState
        """
        queue = self.getQueue(topic)
        if queue is not None:
            for task in queue:
                if task.task_id == task_id:
                    return task.status

        for task in self.success_queue:
            if task.task_id == task_id:
                return task.status  # Return success status

        for task in self.failure_queue:
            if task.task_id == task_id:
                return task.status  # Return failure status

        return TaskState.FAILURE


manager = QueueManager()
