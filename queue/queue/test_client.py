from queue_service import manager
from queue import PriorityQueue, QueueTask
from MyWorker import MyWorker

manager.createQueue("1")

queue = manager.getQueue("1")

task1 = QueueTask(1, "Saurabh1", priority=3)
task2 = QueueTask(1, "Saurabh2", priority=3)
task3 = QueueTask(1, "Saurabh3", priority=3)

queue.enqueue(task1)
queue.enqueue(task2)
queue.enqueue(task3)

worker = MyWorker()
worker.execute()
