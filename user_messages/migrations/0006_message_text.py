# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-13 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_messages', '0005_auto_20170413_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='text',
            field=models.TextField(default=123),
            preserve_default=False,
        ),
    ]
