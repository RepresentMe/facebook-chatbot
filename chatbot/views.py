from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import models
import json
import requests


@csrf_exempt
def webhook(req):
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
                ask_question(m.sender)
    return HttpResponse()
    # print(dir(req))
    # m = models.Message()
    # m.sender = 'Oleg'
    # m.save()


def ask_question(user_id):
    question_req = {
        'recipient': {
            'id': user_id
        },
        'message': {
            'text': 'Test'
        }
    }
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % \
          (
              'EAAVZCyjFh4eEBAF6ox3WSbpiTUI4ksXPCTFLXpK2ZAeT7i85SgWM9aekq1eu8ZBMSCetTqObtl8DYWHPzRMGnYPT2ugwpD394mAZBonciOefHVxtZCiMsOKgYr6o3N5yKCbvuqVCV0Of6wRuoaY4UBH5AzjDPwUwntasI3jqGMgZDZD',)
    response_msg = json.dumps(question_req)
    r = requests.post(url, headers={"Content-Type": "application/json"}, data=response_msg)
    print(r.text)


def misunderstood():
    pass


def last_messages(req):
    return render(req, 'lastmessages.html', {'messages': models.Message.objects.all()})


def index(req):
    return HttpResponse('Hello on chatbot server!')

# Create your views here.
