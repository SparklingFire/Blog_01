from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from user_messages.models import Message
from django.utils import timezone
from articles.models import Subscription, Article
from django.contrib.contenttypes.fields import GenericRelation
from utils_tags_cp.models import Image
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Введите адрес электронной почты')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            password=password
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=25, unique=True)
    username_slug = models.CharField(max_length=25, blank=True, null=True, unique=True)
    email = models.EmailField()
    birthday = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False, verbose_name='activation')
    is_admin = models.BooleanField(default=False, verbose_name='Admin permission')
    objects = CustomUserManager()
    avatar = GenericRelation(Image)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        self.username_slug = self.username.lower()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_user_rating_object(self):
        return self.userratingmodel

    def get_subscription_articles(self):
        return self.get_subscriptions().values_list('article', flat=True)

    def update_subscriptions(self):
        for sub in self.get_subscriptions():
            sub.get_updates()

    def get_subscriptions(self):
        return self.subscription_set.all()

    def get_user_articles(self):
        return self.article_set.all()

    def get_user_comments(self):
        return self.comment_set.all()

    def get_user_tag(self):
        return self.tag_set.all()

    def get_user_rating(self):
        return self.get_user_rating_object().score

    def get_user_likes(self):
        return self.get_user_rating_object().likes

    def get_user_dislikes(self):
        return self.get_user_rating_object().dislikes

    def get_user_unread_messages(self):
        return self.messagelist.receiver_messages.filter(unread=True)

    def get_avatar(self):
        return self.avatar.last().image.url
