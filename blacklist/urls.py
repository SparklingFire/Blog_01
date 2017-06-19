from django.conf.urls import url
from . import views


urlpatterns = [
    url(regex='^block_user/(?P<target>[\w]+)/$',
        view=views.blacklist_user,
        name='blacklist-user')
]