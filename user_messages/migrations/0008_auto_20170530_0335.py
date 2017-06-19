# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-30 00:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_messages', '0007_message_message_list'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='user_author',
            new_name='author_message_list',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='target_user',
            new_name='target_message_list',
        ),
        migrations.AddField(
            model_name='message',
            name='title',
            field=models.CharField(default='123', max_length=50),
            preserve_default=False,
        ),
    ]
