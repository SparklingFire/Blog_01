# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-17 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20170612_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='target_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
