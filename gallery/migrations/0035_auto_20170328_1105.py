# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-28 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0034_auto_20170327_0455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofilemodel',
            name='occupation',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='occupation'),
        ),
    ]