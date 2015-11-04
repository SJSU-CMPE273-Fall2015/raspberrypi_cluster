# Create your tests here.
from .queue import SimpleQueueTask, SimplePriorityQueue, manager

TEST_QUEUE = 'test_queue_1'


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
    q1 = SimpleQueueTask(1, temp)
    q2 = SimpleQueueTask(2, temp)
    q3 = SimpleQueueTask(3, temp)
    q4 = SimpleQueueTask(4, temp, 0)
    q5 = SimpleQueueTask(5, temp, 2)

    queue = SimplePriorityQueue('test', 20)
    queue.enqueue(q1)
    queue.enqueue(q2)
    queue.enqueue(q3)
    queue.enqueue(q4)
    queue.enqueue(q5)

    assert len(queue.heap) == 5

    elem = queue.dequeue()
    assert len(queue.heap) == 4
    print(elem)
    assert elem.priority == 0
    assert elem.task_id == 4

    elem = queue.dequeue()
    assert len(queue.heap) == 3
    assert elem.priority == 2
    assert elem.task_id == 5

    elem = queue.dequeue()
    assert len(queue.heap) == 2
    assert elem.priority == 3
    assert elem.task_id == 1

    elem = queue.dequeue()
    assert len(queue.heap) == 1
    assert elem.priority == 3
    assert elem.task_id == 2


def test_queuemanager():
    success = manager.createQueue(TEST_QUEUE, 10)
    if not success:
        raise AssertionError(TEST_QUEUE + "Queue can not be created")

    queue = manager.getQueue(TEST_QUEUE)
    print(queue)
