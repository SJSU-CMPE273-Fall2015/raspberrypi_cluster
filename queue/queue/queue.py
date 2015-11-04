__author__ = 'saurabh'
import time


class ClusterIdentifier(object):
    def __init__(self, ip, port):
        self.ip = ip;
        self.port = port;


class TaskState(object):
    WAIT = "WAIT"
    IN_PROGRESS = "IN PROGRESS"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"


class QueueTask(object):
    def __init__(self, task_id, data, priority=3):
        self.task_id = task_id
        self.status = TaskState.WAIT
        self.time = time.time()
        self.data = data
        self.priority = priority

    def __str__(self, *args, **kwargs):
        return str(self.task_id) + ":" + str(self.time) + ":" + self.status + ":" + str(self.priority) + ":" + str(
            self.data)

    def __repr__(self):
        return self.__str__()


# def authenticate(func):
#     def authenticate_and_call(*args, **kwargs):
#         print("Hello world222222222!")
#         print(args)
#         print(kwargs)
#         return func(*args, **kwargs)
#
#     return authenticate_and_call
#
#
# @authenticate
# def test(self):
#     print("--------------Hello world!")
#     for i in self:
#         print(i)
#
#
# temp = test
# q = QueueTask(1, temp)
# print(q)
# q.execute()
#

class PriorityQueue(object):
    MAX_PRIORITY = 3

    def __init__(self, queueId):
        self.heap = []
        self.queueId = queueId
        self.healthCheckUp()

    def has_more(self):
        return len(self.heap) > 0

    def enqueue(self, task=QueueTask):
        self.heap.append(task)
        pass

    def pop(self):
        highest_priority = self.MAX_PRIORITY
        iter = 0
        index = 0

        for task in self.heap:
            if task.priority < highest_priority:
                highest_priority = task.priority
                index = iter
            iter += 1
        return self.heap.pop(index)

    # def remove(self, taskId):
    #     for task in self.heap:
    #         if task.task_id == taskId:
    #             self.heap.remove(task)

    def __str__(self):
        return str(self.heap)

    def __repr__(self):
        return self.__str__()

    def healthCheckUp(self):
        print("Checking Queue Health...")
        import time
        for task in self.heap:
            if time.time() - task.time >= 20:
                task.status = TaskState.FAILED
                self.heap.remove(task)
                print("Removed task:", task)
        import threading
        threading.Timer(3.0, self.healthCheckUp).start()
