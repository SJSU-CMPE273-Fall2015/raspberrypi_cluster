from nose.tools import *
from queue.queue import QueueTask, PriorityQueue


def setup():
    print("SETUP!")


def teardown():
    print("TEAR DOWN!")


def test_queue():
    def test(args):
        print("--------------Hello world!")
        for i in args:
            print(i)

    temp = test
    q1 = QueueTask(1, temp)
    q2 = QueueTask(2, temp)
    q3 = QueueTask(3, temp)
    q4 = QueueTask(4, temp, 0, "test")
    q5 = QueueTask(5, temp, 2)

    priorityQueue = PriorityQueue()
    priorityQueue.enqueue(q1)
    priorityQueue.enqueue(q2)
    priorityQueue.enqueue(q3)
    priorityQueue.enqueue(q4)
    priorityQueue.enqueue(q5)

    assert len(priorityQueue.heap) == 5

    elem = priorityQueue.pop()
    assert  len(priorityQueue.heap) == 4
    print(elem)
    assert elem.priority == 0
    assert elem.task_id == 4

    elem = priorityQueue.pop()
    assert  len(priorityQueue.heap) == 3
    assert elem.priority == 2
    assert elem.task_id == 5

    elem = priorityQueue.pop()
    assert  len(priorityQueue.heap) == 2
    assert elem.priority == 3
    assert elem.task_id == 1

    elem = priorityQueue.pop()
    assert  len(priorityQueue.heap) == 1
    assert elem.priority == 3
    assert elem.task_id == 2