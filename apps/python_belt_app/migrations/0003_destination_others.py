# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-18 02:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('python_belt_app', '0002_auto_20191115_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='others',
            field=models.ManyToManyField(related_name='joins', to='python_belt_app.Users'),
        ),
    ]