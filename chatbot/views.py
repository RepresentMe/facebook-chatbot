from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import models, questions
import json


@csrf_exempt
def webhook(req):
    # print(req.body)
    incoming_message = json.loads(req.body)
    for entry in incoming_message['entry']:
        for message in entry['messaging']:
            # Check to make sure the received call is a message call
            # This might be delivery, optin, postback for other events
            if message.has_key('message'):
                questions.process_message(message['sender']['id'], message['message']['text'])
    return HttpResponse()


def last_messages(req):
    return render(req, 'lastmessages.html', {'messages': models.Message.objects.all()})


@csrf_exempt
def test_message(req):
    questions.process_message(req.GET['user_id'], req.GET['text'])
    return HttpResponse(200)


def index(req):
    return HttpResponse('Hello on chatbot server!')

# Create your views here.
