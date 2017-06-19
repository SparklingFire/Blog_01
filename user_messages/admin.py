from django.contrib import admin
from .models import (Message, MessageList)

admin.site.register(Message)
admin.site.register(MessageList)
