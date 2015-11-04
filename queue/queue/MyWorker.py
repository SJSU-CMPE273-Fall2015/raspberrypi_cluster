from BaseWorker import BaseWorker
from queue_service import manager
import time

__author__ = 'saurabh'


class MyWorker(BaseWorker):
    def execute(self):
        queue = manager.getQueue("1")
        while (1):
            if (queue.has_more()):
                task = queue.dequeue()
                print("-----processing task " + str(task.task_id) + "------------")
                print(task)
                print(task.data)
                time.sleep(2)
                print("-------------------------------")
            else:
                print("Queue does not have element.. Sleeping..")
                time.sleep(5)
