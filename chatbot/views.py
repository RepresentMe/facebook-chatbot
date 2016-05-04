from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import models
import json


@csrf_exempt
def webhook(req):
    m = models.Message()
    m.sender = '123'#str(req.body)
    # m.text = message['message']['text']
    m.save()
    # Post function to handle Facebook messages
    # Converts the text payload into a python dictionary
    incoming_message = json.loads(req.body)
    # Facebook recommends going through every entry since they might send
    # multiple messages in a single call during high load
    for entry in incoming_message['entry']:
        for message in entry['messaging']:
            # Check to make sure the received call is a message call
            # This might be delivery, optin, postback for other events
            if message.has_key('message'):
                # Print the message to the terminal
                m = models.Message()
                m.sender = message['sender']['id']
                m.text = message['message']['text']
                m.save()
    return HttpResponse()
    # print(dir(req))
    # m = models.Message()
    # m.sender = 'Oleg'
    # m.save()
    return JsonResponse({'status': 'ok'})


def last_messages(req):
    return render(req, 'lastmessages.html', {'messages': models.Message.objects.all()})


def index(req):
    return HttpResponse('Hello on chatbot server!')

# Create your views here.
