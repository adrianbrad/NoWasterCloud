# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-29 13:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noWaster', '0021_remove_user_last_update_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_update_time',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
