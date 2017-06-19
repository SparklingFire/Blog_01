from tag.models import Tag
from articles.forms import SearchForm
from articles.models import (Article, Subscription)
from comments.models import Comment


def popular_articles(request):
    articles = Article.objects.get_popular_articles()[:5]
    return {'POPULAR_ARTICLES': articles}


def subscriptions(request):
    if request.user.is_authenticated:
        subscription_list = Subscription.objects.filter(subscribed_user=request.user)
    else:
        subscription_list = Subscription.objects.filter(session=request.session.session_key)
    return {"SUBSCRIPTION_LIST": subscription_list}


def tag_list(request):
    tags = Tag.objects.all()
    return {"TAGS": tags}


def search_form(request):
    form = SearchForm
    return {"SEARCH_FORM": form}


def recent_comments(request):
    return {"RECENT_COMMENTS": Comment.objects.recent_comments()}
