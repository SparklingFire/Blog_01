from django.conf.urls import url
from user_messages import views


urlpatterns = [
    url(regex='^message_list/(?P<label>[-\w]+)/$',
        view=views.MessagesList.as_view(),
        name='messages-list'
        ),

    url(regex='^send_message/(?P<username>[-\w]+)/$',
        view=views.SendMessage.as_view(),
        name='send-message'),
]