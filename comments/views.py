from django.shortcuts import render
from articles.views import ajax_call


def comment_refresh(request):
    if request.method == 'POST':
        print(request.POST)

