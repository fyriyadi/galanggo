# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-28 11:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gallery', '0035_auto_20170328_1105'),
    ]

    operations = [
        migrations.CreateModel(
            name='VolunteerStatusModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=200, verbose_name='status')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_volunteers', to='gallery.ProjectModel')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_volunteers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]