# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-26 17:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noWaster', '0010_loc_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loc',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='loc',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
