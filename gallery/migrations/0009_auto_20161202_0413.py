# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-02 04:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0008_responsemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmodel',
            name='dana_dibutuhkan',
            field=models.CharField(default=0, max_length=200, verbose_name='dana dibutuhkan'),
        ),
        migrations.AlterField(
            model_name='projectmodel',
            name='dana_terkumpul',
            field=models.CharField(default=0, max_length=200, verbose_name='dana terkumpul'),
        ),
    ]
