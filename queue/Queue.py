__author__ = 'saurabh'
import time


class QueueTask(object):
    def __init__(self, task_id, task):
        self.task_id = task_id
        self.status = "Wait"
        self.time = time.time()
        self.task = task

    def execute(self):
        self.task()

    def __str__(self, *args, **kwargs):
        return str(self.task_id) + ":" + str(self.time) + ":" + self.status

def authenticate(func):
    def authenticate_and_call(*args, **kwargs):
        if not Account.is_authentic(request):
            raise Exception('Authentication Failed.')
        return func(*args, **kwargs)

    return authenticate_and_call

@authenticate
def test():
    print("Hello world!")


temp = test
q = QueueTask(1, temp)
print(q)
q.execute()



