# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-05-07 10:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0065_auto_20190425_1127'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='game',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='game',
            name='project',
        ),
        migrations.DeleteModel(
            name='Game',
        ),
    ]
