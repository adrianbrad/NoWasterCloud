# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-27 17:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noWaster', '0015_auto_20180327_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dest_loc_address',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='origin_loc_address',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
