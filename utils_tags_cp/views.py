from django.http import JsonResponse
from user_messages.models import MessageList, Message
from articles.models import Subscription
import json


def update_user_info(request):
    if request.is_ajax():
        data = {}
        data.update({'user_rating': request.user.userratingmodel.score})
        data.update({'unread_messages': request.user.get_user_unread_messages().count()})
        data.update({'subscriptions': json.dumps({x.article.primary_key: x.new_comments for x
                                                  in Subscription.objects.filter(subscribed_user=request.user)})})
        return JsonResponse(data)
