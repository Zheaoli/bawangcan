# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-12 12:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bawangcan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bawangcanstatus',
            name='status_end_time',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='bawangcanstatus',
            name='status_start_time',
            field=models.IntegerField(),
        ),
    ]
