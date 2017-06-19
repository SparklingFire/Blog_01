from django.shortcuts import redirect, HttpResponseRedirect
from .models import (Vote)
from comments.models import Comment
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from utils_tags_cp.utils import get_ip


def rating_view(request, pk, vote):

    like = True if vote == 'like' else False

    try:
        rating_model = Comment.objects.get(pk=pk).get_rating_model()
    except ObjectDoesNotExist:
        redirect('gag')

    if request.user.is_authenticated():
        user = request.user
    else:
        user = None

    """
       The view tries to get a vote object with existing parameters. If it's found, the object is going to be
       deleted or changed. If not, just create one more Vote object.
    """

    try:
        if user:
            vote = Vote.objects.get(rating_model=rating_model,
                                    user=user)
        else:
            vote = Vote.objects.get(session=request.session.session_key,
                                    ip=get_ip(request),
                                    rating_model=rating_model)
        if vote.like == like:
            vote.delete()
        else:
            vote.like = like
            vote.save()

    except ObjectDoesNotExist:
        Vote.objects.create(session=request.session.session_key,
                            ip=get_ip(request),
                            like=like,
                            rating_model=rating_model,
                            user=user)

    rating_model.calculate_score()
    if request.is_ajax():
        return JsonResponse({'likes': str(rating_model.likes),
                             'dislikes': str(rating_model.dislikes),
                             'like': like})

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
