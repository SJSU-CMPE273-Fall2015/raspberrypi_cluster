__author__ = 'saurabh'
import time


class QueueTask(object):
    def __init__(self, task_id, task, priority=3, *args):
        self.task_id = task_id
        self.status = "Wait"
        self.time = time.time()
        self.task = task
        self.args = args
        self.priority = priority

    def execute(self):
        self.task(self.args)

    def __str__(self, *args, **kwargs):
        return str(self.task_id) + ":" + str(self.time) + ":" + self.status + ":" + str(self.priority) + ":" + str(
            self.args)

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
    def __init__(self):
        self.heap = []

    def enqueue(self, task=QueueTask):
        self.heap.append(task)
        pass

    def pop(self):
        highest_priority = 3
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
