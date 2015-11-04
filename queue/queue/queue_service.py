__author__ = 'saurabh'
from queue import PriorityQueue, QueueTask


class QueueManager(object):
    def __init__(self):
        self.queues = {}

    def getQueue(self, queueId):
        print(self.queues)
        return self.queues.get(queueId)

    def createQueue(self, queueId):
        queue = PriorityQueue(10)
        self.queues[queueId] = queue


manager = QueueManager()
