# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-31 16:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='khanuser',
            name='is_infected',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='khanuser',
            name='mockaroo_id',
            field=models.CharField(max_length=200),
        ),
    ]
