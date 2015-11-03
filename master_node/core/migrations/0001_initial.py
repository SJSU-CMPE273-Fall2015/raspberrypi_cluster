# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField(null=True)),
                ('location', models.CharField(max_length=255, null=True)),
                ('type', models.CharField(max_length=255, null=True)),
                ('last_boot_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClusterProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=255, null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('cluster', models.ForeignKey(to='core.Cluster', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_name', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=255, null=True)),
                ('last_build_time', models.DateTimeField(auto_now=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectAudit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=255, null=True)),
                ('tag', models.CharField(max_length=255, null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(to='core.Project', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectBuild',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('build', models.BinaryField(null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(to='core.Project', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SystemAudit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('disk_usage', models.FloatField(null=True)),
                ('memory_usage', models.FloatField(null=True)),
                ('cpu_usage', models.FloatField(null=True)),
                ('network_usage', models.FloatField(null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('cluster', models.ForeignKey(to='core.Cluster', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('lname', models.CharField(max_length=255, null=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(to='core.User', null=True),
        ),
        migrations.AddField(
            model_name='clusterproject',
            name='project',
            field=models.ForeignKey(to='core.Project', null=True),
        ),
    ]
