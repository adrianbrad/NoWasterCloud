# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-26 16:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noWaster', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(db_column=b'ID', primary_key=True, serialize=False),
        ),
    ]