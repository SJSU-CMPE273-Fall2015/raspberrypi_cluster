from django.db import models


# Create your models here.

class RQueue(models.Model):
    topic = models.CharField(max_length=256)


class QueueTask(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    data = models.CharField(max_length=1024)

    LOW_PRIORITY = 3
    MED_PRIORITY = 2
    HIGH_PRIORITY = 1
    EMERGENCY = 0

    PRIORITY = ((LOW_PRIORITY, 'LOW'), (MED_PRIORITY, 'MED'), (HIGH_PRIORITY, 'HIGH'), (EMERGENCY, 'EMERGENCY'))
    priority = models.CharField(max_length=1, choices=PRIORITY, default=MED_PRIORITY)

    PENDING = 'PENDING'
    STARTED = 'STARTED'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'

    STATUS = (
        (PENDING, 'PENDING'),
        (STARTED, 'STARTED'),
        (SUCCESS, 'SUCCESS'),
        (FAILURE, 'FAILURE'),
    )
    status = models.CharField(max_length=15, choices=STATUS, default=PENDING)
    queue = models.ForeignKey('RQueue', blank=True, null=True, )

    def __repr__(self):
        pass

    def __str__(self, *args, **kwargs):
        return str(self.task_id) + ":" + str(self.time) + ":" + self.status + ":" + self.priority + ":" + self.data
