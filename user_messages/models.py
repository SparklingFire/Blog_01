from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models import Q


class MessageList(models.Model):
    created = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(default=timezone.now)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    counter = models.SmallIntegerField(default=0)
    unread_messages = models.SmallIntegerField(default=0)

    def __str__(self):
        return 'Message list of user {0}'.format(self.user)

    def update_counters(self):
        messages = Message.objects.filter(Q(sender_message_list=self) | Q(receiver_message_list=self))
        self.counter = messages.count()
        self.unread_messages = messages.filter(unread=True).count()
        return self.save()


class Message(models.Model):
    title = models.CharField(max_length=50)
    created = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(default=timezone.now)
    sender_message_list = models.ForeignKey(MessageList, blank=True, null=True, related_name='sender_messages')
    receiver_message_list = models.ForeignKey(MessageList, blank=True, null=True, related_name='receiver_messages')
    text = models.TextField()
    unread = models.BooleanField(default=True)

    def __str__(self):
        return 'Message from {0} to {1}'.format(self.sender_message_list.user, self.receiver_message_list.user)
