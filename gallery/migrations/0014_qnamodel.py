# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-02 23:09
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0013_auto_20161205_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='QnAModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('konteks', models.CharField(default='', max_length=1024, verbose_name='konteks QnA')),
                ('pertanyaan', models.CharField(default='', max_length=1024, verbose_name='pertanyaan QnA')),
                ('jawaban', wagtail.wagtailcore.fields.RichTextField(default='', max_length=1024, verbose_name='jawaban QnA')),
            ],
        ),
    ]