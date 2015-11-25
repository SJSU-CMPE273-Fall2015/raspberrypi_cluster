# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectbuild',
            name='log',
            field=models.TextField(default=datetime.datetime(2015, 11, 22, 21, 30, 32, 905280, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='projectbuild',
            name='build',
            field=models.FileField(upload_to='', null=True),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
