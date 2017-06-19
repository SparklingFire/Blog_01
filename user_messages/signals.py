from custom_user.models import CustomUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import (Message, MessageList)
from django.db.models import Q


@receiver(post_save, sender=CustomUser)
def create_user_messages_list(sender, instance, **kwargs):
    MessageList.objects.get_or_create(user=instance)


@receiver(post_save, sender=Message)
@receiver(post_delete, sender=Message)
def update_messages_counter(sender, instance, **kwargs):

    for messages_list in (instance.sender_message_list, instance.receiver_message_list):
        messages_list.update_counters()
