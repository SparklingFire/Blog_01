from django.shortcuts import render, get_object_or_404, reverse, redirect, Http404
from django.contrib.auth import logout, login, authenticate
from django.views import generic
from django.http import JsonResponse
from .forms import LoginForm
from .models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain


class LogoutView(generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return self.request.META.get('HTTP_REFERER','/')

    def dispatch(self, request, *args, **kwargs):
        logout(self.request)
        return super().dispatch(request, *args, **kwargs)


class LoginView(generic.FormView):
    form_class = LoginForm
    template_name = 'user/login.html'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')

    def form_invalid(self, form):
        if self.request.is_ajax:
            print(form.errors)
            return JsonResponse({'errors': form.errors})
        else:
            return super().form_invalid(form)

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        )
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(reverse('article-list'))
        return super().dispatch(request, *args, **kwargs)


class UserInfoView(generic.TemplateView):
    user = None
    template_name = 'user/user_info.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['username'] = self.user.username
        ctx['likes'] = self.user.get_user_likes
        ctx['dislikes'] = self.user.get_user_dislikes
        ctx['avatar'] = self.user.get_avatar
        ctx['created'] = self.user.birthday
        ctx['recent_activity'] = sorted(chain(self.user.article_set.all(),
                                              self.user.comment_set.all()),
                                        key=lambda x: x.created
                                        )
        ctx['auth_user'] = self.request.user.username
        return ctx

    def dispatch(self, request, *args, **kwargs):
        self.user = CustomUser.objects.get(username=kwargs['username'])
        return super().dispatch(request, *args, **kwargs)


def check_auth(request):
    data = {}
    if request.is_ajax():
        if request.user.is_authenticated():
            data.update({'auth': 'true'})
        else:
            data.update({'auth': 'false'})
    return JsonResponse(data)


def change_avatar(request, username):
    try:
        CustomUser.objects.get(username=username)
    except ObjectDoesNotExist:
        pass
