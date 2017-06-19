# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-28 02:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_messages', '0006_message_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_list',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user_messages.MessageList'),
            preserve_default=False,
        ),
    ]
