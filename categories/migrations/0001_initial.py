# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2014, 9, 7, 18, 0, 27, 488709), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 9, 7, 18, 0, 27, 488731), auto_now=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
    ]
