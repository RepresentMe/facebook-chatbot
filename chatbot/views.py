from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import models, questions
import json

from django.conf import settings


@csrf_exempt
def webhook(req):

    incoming_message = json.loads(req.body)
    for entry in incoming_message['entry']:
        for message in entry['messaging']:
            if message.has_key('message'):
                questions.process_message(message['sender']['id'], message['message']['text'])
    return HttpResponse()


def last_messages(req):
    return render(req, 'lastmessages.html', {'messages': models.Message.objects.all()})


def last_messages_by_id(req, id):
    return render(req, 'lastmessages.html', {'messages': models.Message.objects.all().filter(sender=id)})


@csrf_exempt
def test_message(req):
    if settings.DEBUG:
        user = 0
        if 'user_id' in req.GET:
            questions.process_message(req.GET['user_id'], req.GET['text'])
            user = req.GET['user_id']

        return render(req, 'test_message.html', {'user_id': user})
    else:
        return HttpResponse(403)


def index(req):
    return HttpResponse('Hello on chatbot server!')

# Create your views here.
