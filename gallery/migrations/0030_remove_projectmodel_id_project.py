# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-26 10:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0029_auto_20170326_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectmodel',
            name='id_project',
        ),
    ]
