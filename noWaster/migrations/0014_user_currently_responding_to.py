# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-27 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noWaster', '0013_auto_20180327_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='currently_responding_to',
            field=models.BooleanField(default=False),
        ),
    ]
