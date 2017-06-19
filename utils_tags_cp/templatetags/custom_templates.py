from django import template
from django.template.loader import get_template
from user_messages.forms import SendMessageForm
from password.forms import PasswordChangeForm
from utils_tags_cp.forms import ChangeAvatar
from custom_user.forms import LoginForm
from registration.forms import RegistrationForm
from user_messages.forms import SendMessageForm
from django.db.models import Q


register = template.Library()


@register.simple_tag(name='password_change', takes_context=True)
def password_change_form(context):
    request = context['request']
    return PasswordChangeForm(user=request.user)


@register.simple_tag(name='avatar_form')
def change_avatar_form():
    return ChangeAvatar()


@register.simple_tag(name='login')
def login_form():
    return LoginForm()


@register.simple_tag(name='registration')
def registration_form():
    return RegistrationForm()


@register.simple_tag(name='send_message')
def message_form():
    return SendMessageForm()
