# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-13 07:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bawangcan', '0007_bawangcanstatus_status_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bawangcanstatus',
            name='status_type',
            field=models.IntegerField(),
        ),
    ]
