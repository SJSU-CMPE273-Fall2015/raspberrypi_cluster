__author__ = 'saurabh'


class BaseWorker(object):
    def execute(self):
        raise NotImplementedError
