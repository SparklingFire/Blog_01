# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-13 17:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_messages', '0004_remove_messageroom_room_preview'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('edited', models.DateTimeField(default=django.utils.timezone.now)),
                ('counter', models.SmallIntegerField(default=0)),
                ('unread_messages', models.SmallIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='messageroom',
            name='messages_list',
        ),
        migrations.RemoveField(
            model_name='messageroom',
            name='participant',
        ),
        migrations.RemoveField(
            model_name='messageslist',
            name='user',
        ),
        migrations.RemoveField(
            model_name='message',
            name='message_room',
        ),
        migrations.RemoveField(
            model_name='message',
            name='text',
        ),
        migrations.RemoveField(
            model_name='message',
            name='user',
        ),
        migrations.AlterField(
            model_name='message',
            name='target_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Target_User', to='user_messages.MessageList'),
        ),
        migrations.DeleteModel(
            name='MessageRoom',
        ),
        migrations.DeleteModel(
            name='MessagesList',
        ),
        migrations.AddField(
            model_name='message',
            name='user_author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Author_User', to='user_messages.MessageList'),
        ),
    ]
