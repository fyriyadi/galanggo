# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-05 13:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0011_auto_20161205_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donationmodel',
            name='handphone',
        ),
        migrations.AddField(
            model_name='donationmodel',
            name='telephone',
            field=models.CharField(default='', max_length=1024, verbose_name='telephone donatur'),
        ),
    ]
