from django.shortcuts import reverse, HttpResponseRedirect, Http404, get_object_or_404, render, redirect
from django.views import generic
from .models import (Article, Subscription)
from django.db.models import Q
from tag.models import Tag
from hit import models as hit_models
from django.core.exceptions import ObjectDoesNotExist
from rating.models import RatingModel
from comments.forms import CommentForm
from comments.models import Comment
from utils_tags_cp.utils import get_ip
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from utils_tags_cp.forms import ChangeAvatar
from utils_tags_cp.forms import Image
from tag.forms import TagForm
from django.utils import formats
import json


def ajax_call(request, comment, parent=None):
    data = {'rating_model_pk': comment.get_rating_model_pk(),
            'comment_text': comment.text,
            'comment_name': comment.name,
            'datetime': formats.date_format(comment.created, "SHORT_DATETIME_FORMAT"),
            'auth_user': False,
            'comment_pk': comment.id,
            'parent': None,
            'username': 'Аноним',
            'likes': comment.get_likes(),
            'dislikes': comment.get_dislikes(),
            'session': comment.session,
            'login_user': request.user.username,
            'current_session': request.session.session_key,
            'blacklisted': False,
            'target_name': None
            }
    if comment.author:
        data.update({'avatar': comment.author.get_avatar()})
    else:
        data.update({'avatar': None})

    if comment.author:
        data.update({'auth_user': True,
                     'username': comment.author.username,
                     })

    if comment.parent or parent:
        data.update({'parent': comment.parent.name,
                     'parent_id': comment.parent.pk,
                     'target_name': comment.target_name
                     })
    try:
        data.update({'check_color': comment.get_rating_model().vote_set.get(Q(user=request.user)
                                                                   | Q(session=request.session)).like})
    except ObjectDoesNotExist:
        pass

    if comment.author.pk in request.user.blacklist.blacklisteduser_set.values_list('user', flat=True):
        data.update({'blacklisted': True})

    return data


class ArticlesList(generic.ListView):
    template_name = 'main_page/article_list.html'
    paginate_by = 12
    search_list = Article.objects.all().order_by('-created')
    tag = None

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            articles = []
            for object in context.get('object_list'):
                articles.append({'title': object.title,
                                 'created': object.created,
                                 'primary_key': object.primary_key,
                                 'image_object': object.get_image()})
            return JsonResponse(articles, safe=False)
        return render(self.request, 'main_page/article_list.html', context)

    def get_queryset(self):
        """
        returns queryset that depends on the Article fields
        """
        if self.tag:
            try:
                return Tag.get_articles_by_tag(self.tag)
            except ObjectDoesNotExist:
                raise Http404
        return self.search_list

    def dispatch(self, request, *args, **kwargs):
        """
        Check if the request is a form request or is a tag request. Fill the target field
        """

        if 'q' in request.GET:
            self.search_list = Article.objects.filter(Q(title__contains=request.GET['q']) |
                                                      Q(text__contains=request.GET['q'])
                                                      )
        if 'tag' in kwargs:
            self.tag = kwargs['tag']

        return super().dispatch(request, *args, **kwargs)


class ArticleDetails(generic.FormView):
    template_name = 'main_page/article_details.html'
    article = None
    form_class = CommentForm

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs.update({'session': self.request.session.session_key,
                            'article': self.article}
                           )
        return form_kwargs

    def get_success_url(self):
        return reverse('article-details', args=[self.article.primary_key])

    def get_context_data(self, **kwargs):
        ctx = super(ArticleDetails, self).get_context_data(**kwargs)
        ctx['article'] = self.article
        ctx['subscription'] = None
        if self.request.user.is_authenticated:
            ctx['blacklist'] = self.request.user.blacklist.blacklisteduser_set.values('user')
        try:
            ctx['subscription'] = Subscription.objects.get(subscribed_user=self.request.user, article=self.article)
        except (ObjectDoesNotExist, TypeError):
            try:
                ctx['subscription'] = Subscription.objects.get(session=self.request.session.session_key, article=self.article)
            except ObjectDoesNotExist:
                pass
        return ctx

    def form_invalid(self, form):
        if self.request.is_ajax:
            return JsonResponse({'errors': form.errors})
        else:
            return super().form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        parent = form['parent'].value()
        if parent:
            comment.parent = Comment.objects.get(pk=int(parent))
        comment.article = self.article
        comment.session = self.request.session.session_key
        comment.ip = get_ip(self.request)
        if self.request.user.is_authenticated():
            comment.author = self.request.user
            comment.published = True
        comment.save()
        try:
            subscription_list = Subscription.objects.filter(article=self.article)\
                .exclude(subscribed_user=self.request.user)
        except TypeError:
            subscription_list = Subscription.objects.filter(article=self.article)
        for sub in subscription_list:
            sub.new_comments += 1
            sub.total_comments += 1
            sub.save()

        if self.request.is_ajax():
            data = ajax_call(self.request, comment, parent)
            return JsonResponse(data)
        response = super().form_valid(form)
        return response

    def dispatch(self, request, *args, **kwargs):

        try:
            self.article = Article.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('gag'))
        """
        Checks if the model has a hitctcount model and a rating model.
        Adds a hit to an existing hitcount model for that article
        """

        try:
            hit_count_model = self.article.hitcount
        except AttributeError:
            hit_count_model = hit_models.HitCount.objects.create(article=self.article)

        if not self.article.rating_object.last():
            RatingModel.objects.create(content_object=self.article)

        if not request.session.exists(request.session.session_key):
            request.session.create()

        hit_models.Hit.objects.get_or_create(session=request.session.session_key,
                                             hitcount=hit_count_model,
                                             ip=get_ip(self.request))
        try:
            if self.request.user.is_authenticated:
                subscription = Subscription.objects.get(article=self.article, subscribed_user=self.request.user)

            else:
                subscription = Subscription.objects.get(article=self.article, session=self.request.session.session_key)
            subscription.new_comments = 0
            subscription.checked_comments = subscription.total_comments
            subscription.save()
        except ObjectDoesNotExist:
            pass
        return super().dispatch(request, *args, **kwargs)


def load_comments(request, article_pk):
    current_comments = json.loads(request.POST.get('data'))
    article = Article.objects.get(primary_key=article_pk)
    comments = []
    for comment in article.comment_set.exclude(id__in=current_comments):
        new_comment = ajax_call(request, comment)
        comments.append(new_comment)
    return JsonResponse(comments, safe=False)


def edit_comment(request, id):
    comment = Comment.objects.get(pk=id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, session=request.session.session_key, article=comment.article)
        if comment_form.is_valid():
            comment.text = comment_form.cleaned_data.get('text')
            comment.save()
        else:
            return JsonResponse({'errors': comment_form.errors})
    return JsonResponse({'message': ''})


class SiteInfo(generic.TemplateView):
    template_name = 'main_page/static_templates/site_info.html'


class Contacts(generic.TemplateView):
    template_name = 'main_page/static_templates/contacts.html'


class ErrorGag(generic.TemplateView):
    template_name = 'main_page/static_templates/gag.html'


class SubscriptionManagement(generic.RedirectView):
    article = None

    def get_redirect_url(self, *args, **kwargs):
        return self.article.get_absolute_url()

    def dispatch(self, request, *args, **kwargs):
        data = {}
        self.article = get_object_or_404(Article, primary_key=kwargs['primary_key'])
        try:
            sub = Subscription.objects.get(session=request.session.session_key,
                                           ip=get_ip(request),
                                           article=self.article,
                                           subscribed_user=self.request.user)
            data.update({'article': self.article.primary_key})
            sub.delete()
            data.update({'message': 'подписаться'
                         })

        except ObjectDoesNotExist:
            sub = Subscription.objects.create(session=request.session.session_key,
                                              ip=get_ip(request),
                                              article=self.article,
                                              subscribed_user=self.request.user)
            data.update({'sub_id': sub.pk,
                         'message': 'отписаться',
                         'article': self.article.primary_key,
                         'article_title': self.article.title
                         })

        if self.request.is_ajax():
            return JsonResponse(data)

        return super().dispatch(request, *args, **kwargs)


class SubscriptionRefresher(generic.RedirectView):
    pass


@login_required
def delete_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except ObjectDoesNotExist:
        if request.is_ajax():
            return JsonResponse({'message': 'Сообщение не существует'})
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    url = comment.article.get_absolute_url()
    comment.delete()
    if request.is_ajax():
        return JsonResponse({'message': 'Сообщение удалено'})
    return HttpResponseRedirect(url)


def delete_subscription(request, pk):
    subscription = Subscription.objects.get(pk=pk)
    data = {'pk': subscription.article.primary_key,
            'message': 'Подписаться',
            }
    subscription.delete()
    data.update({'sub_counter': Subscription.objects.filter(session=request.session.session_key).count()})

    if request.is_ajax():
        return JsonResponse(data)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def delete_article(request, article_pk):
    try:
        Article.objects.get(pk=article_pk).delete()
    except ObjectDoesNotExist:
        pass
    return HttpResponseRedirect('/')


@login_required()
def create_article(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        tag_form = TagForm(request.POST)
        image_form = ChangeAvatar(request.POST, request.FILES)

        if article_form.is_valid() and tag_form.is_valid() and image_form.is_valid():
            article = Article.objects.create(title=article_form.cleaned_data.get('title'),
                                             text=article_form.cleaned_data.get('text'),
                                             author=request.user)

            for form in (x for x in tag_form.cleaned_data.get('tag_list').split(';') if x):
                new_tag = Tag.objects.get_or_create(tag=form.strip(' '))[0]
                new_tag.user.add(request.user)
                new_tag.article.add(article)
                new_tag.save()

            Image.objects.create(content_object=article, image=image_form.cleaned_data.get('image'))

            return redirect(reverse('article-details', args=[article.primary_key]))
        else:
            if request.is_ajax():
                return
    else:
        article_form = ArticleForm()
        tag_form = TagForm()
        image_form = ChangeAvatar()

    return render(request, 'main_page/create_article.html', {'article_form': article_form,
                                                             'tag_form': tag_form,
                                                             'image_form': image_form
                                                             })


@login_required()
def update_article(request, pk):
    article = Article.objects.get(primary_key=pk)

    if request.user != article.author:
        raise Http404

    if request.method == 'POST':
        article_form = ArticleForm(request.POST, article=article)
        tag_form = TagForm(request.POST)

        if article_form.is_valid() and tag_form.is_valid():
            article.text = article_form.cleaned_data.get('text')
            article.title = article_form.cleaned_data.get('title')
            article.save()
            old_tags = article.get_article_tags()
            new_tags = []

            for form in (x for x in tag_form.cleaned_data.get('tag_list').split(';') if x):
                new_tag = Tag.objects.get_or_create(tag=form.strip(' '))[0]
                new_tag.user.add(request.user)
                new_tag.article.add(article)
                new_tag.save()
                new_tags.append(new_tag)

            for tag in [tag for tag in old_tags if tag not in new_tags]:
                tag.article.remove(article)
                if tag.article.all().count() == 0:
                    tag.delete()

            return redirect(reverse('article-details', args=[article.primary_key]))

    else:
        article_form = ArticleForm(initial={'text': article.text,
                                            'title': article.title,
                                            'author': article.author})
        tag_form = TagForm()

    return render(request, 'main_page/create_article.html', {'article_form': article_form,
                                                             'tag_form': tag_form})
