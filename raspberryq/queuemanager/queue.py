__author__ = 'saurabh'
import json
import time
import threading
import uuid


# If pubsub model is implemented, this will be required
#
# class ClusterIdentifier(object):
#     def __init__(self, ip, port):
#         self.ip = ip;
#         self.port = port;

LOGGER_TIMER = 5
HEALTH_CHECKUP_TIMER = 5
JOB_TIMEOUT = 60


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
    def __init__(self, data, task_id=0, priority=3):

        if task_id is not 0:
            self.task_id = task_id
        else:
            self.task_id = uuid.uuid4().int & (1 << 32) - 1

        self.status = TaskState.PENDING
        self.time = time.time()
        self.data = data
        self.priority = priority

    def __str__(self, *args, **kwargs):
        return self.to_JSON()

    def __repr__(self):
        return self.__str__()

    def __del__(self):
        print("DELETING**************")

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class SimplePriorityQueue(object):
    MAX_PRIORITY = PRIORITY.LOW_PRIORITY

    def __init__(self, topic, size, requireHealthCheckup=True):
        self.heap = []
        self.topic = topic
        self.size = size
        if requireHealthCheckup:
            self.healthCheckUp(HEALTH_CHECKUP_TIMER)

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
        """
        Method updates task state to started and return eligible task
        :return:
        """
        if not self.has_more():
            return None

        highest_priority = self.MAX_PRIORITY

        iter = 0
        index = 0

        for task in self.heap:
            if task.status == TaskState.STARTED:
                iter += 1
                index = iter
                continue

            if task.priority < highest_priority and task.status != "STARTED":
                highest_priority = task.priority
                index = iter
            iter += 1

        if index < len(self.heap):
            self.heap[index].status = TaskState.STARTED
            return self.heap[index]
        return '{"error":"No pending task in queue"}'

    def pop(self):
        """
        Method pops element.
        :return:
        """
        if not self.has_more():
            return None

        highest_priority = self.MAX_PRIORITY

        iter = 0
        index = 0

        for task in self.heap:
            if task.status == TaskState.STARTED:
                iter += 1
                index = iter
                continue

            if task.priority < highest_priority and task.status != "STARTED":
                highest_priority = task.priority
                index = iter
            iter += 1

        if index < len(self.heap):
            self.heap[index].status = TaskState.STARTED
            return self.heap.pop(index)
        return '{"error":"No pending task in queue"}'

    def __str__(self):
        return str(self.heap)

    def __repr__(self):
        return self.topic.join(self.heap)

    def healthCheckUp(self, timer):
        """
        Method to check health of the queue. If Task is timed out, removes it and put it in failure queue.
        Runs periodically.

        """
        # TODO This thread becomes zombie. Correct implementation needed.
        for task in self.heap:
            if time.time() - task.time >= JOB_TIMEOUT:
                task.status = TaskState.FAILURE
                manager.failure_queue.enqueue(task)
                self.heap.remove(task)
                print("Removed task:", task, " from ", self.topic)
        threading.Timer(timer, self.healthCheckUp, [timer]).start()


class QueueManager(object):
    def __init__(self):
        """
        Initializes queue dictionary. Adds two must present queues for success and failure.

        """
        self.queues = {'success': SimplePriorityQueue('success', 500, False),
                       'failure': SimplePriorityQueue('failure', 500, False), }
        self.success_queue = self.queues['success']
        self.failure_queue = self.queues['failure']
        self.logger(LOGGER_TIMER)

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

    def removeQueue(self, topic):
        if topic in self.queues:
            self.queues.pop(topic, None)
            return True
        return False

    def enqueue(self, topic, task):
        queue = self.getQueue(topic)
        if queue is None:
            return False
        return queue.enqueue(task)

    def dequeue(self, topic):
        queue = self.getQueue(topic)
        if queue is None:
            return False
        task = queue.dequeue()
        return task

    def addToSuccessQueue(self, topic, task_id):
        if topic not in self.queues:
            return False
        for task in self.queues[topic].heap:
            if task.task_id == task_id:
                temp = task
                temp.status = TaskState.SUCCESS
                self.success_queue.enqueue(temp)
                self.queues[topic].heap.remove(task)
                return True
        return False

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
            for task in queue.heap:
                if task.task_id == task_id:
                    return task.status

        for task in self.success_queue.heap:
            if task.task_id == task_id:
                return task.status  # Return success status

        for task in self.failure_queue.heap:
            if task.task_id == task_id:
                return task.status  # Return failure status

        return "NOT_FOUND"

    def logger(self, timer):
        """
        Method to print present queues.
        Runs periodically.

        """
        print(time.time())
        for topic in self.queues:
            print(topic)
            print(self.queues[topic])

        # TODO This thread becomes zombie. Correct implementation needed.
        threading.Timer(timer, self.logger, [timer]).start()


manager = QueueManager()
