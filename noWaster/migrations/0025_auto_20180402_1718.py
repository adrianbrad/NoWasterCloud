# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-02 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noWaster', '0024_auto_20180402_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherdictionary',
            name='description',
            field=models.CharField(max_length=50),
        ),
    ]
