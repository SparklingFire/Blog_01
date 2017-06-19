from django.conf.urls import url
from .views import rating_view

urlpatterns = [
    url('^rate/(?P<pk>[0-9]+)/(?P<vote>[\w]+)/$',
        view=rating_view,
        name='like')
]
