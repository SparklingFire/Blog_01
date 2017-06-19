from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from user_messages.models import Message
from user_messages.forms import SendMessageForm
from custom_user.models import CustomUser


class MessagesList(generic.ListView):
    template_name = 'user_messages/message_list.html'
    label = None
    paginate_by = 10
    context_object_name = 'messages'

    def ajax_call(self, message):
        data = {
            'title': message.title,
            'text': message.text,
            'created': message.created,
            'sender': message.sender_message_list.user.username,
            'receiver': message.receiver_message_list.user.username,
            'unread': message.unread,
            'sender_avatar': message.sender_message_list.user.get_avatar(),
            'receiver_avatar': message.receiver_message_list.user.get_avatar(),
            'id': message.pk
        }

        return data

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            messages = []
            for message in context.get('messages'):
                messages.append(self.ajax_call(message))
            return JsonResponse(messages, safe=False)
        else:
            return render(self.request, 'user_messages/message_list.html', context)

    def get_queryset(self):
        user = self.request.user
        return user.messagelist.sender_messages.all()

    def dispatch(self, request, *args, **kwargs):
        self.label = kwargs['label']
        return super().dispatch(request, *args, **kwargs)


class SendMessage(generic.FormView):
    template_name = 'user_messages/send_message.html'
    user = None
    form_class = SendMessageForm

    def form_invalid(self, form):
        if self.request.is_ajax:
            return JsonResponse({'errors': form.errors})
        else:
            return super().form_invalid(form)

    def form_valid(self, form):
        Message.objects.create(title=form.cleaned_data.get('title'),
                               text=form.cleaned_data.get('text'),
                               sender_message_list=self.request.user.messagelist,
                               receiver_message_list=CustomUser.objects.get(username=self.user).messagelist
                               )
        if self.request.is_ajax:
            return JsonResponse({'success_message': 'сообщение отправлено'})
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.user = kwargs.pop('username')
        return super().dispatch(request, *args, **kwargs)


def delete_messages(request, filter):
    pass
