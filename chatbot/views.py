from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import models


@csrf_exempt
def webhook(req):
    m = models.Message()
    m.sender = str(req.POST)
    #m.text = message['message']['text']
    m.save()
    if 'hub.verify_token' in req.GET and req.GET['hub.verify_token'] == 'test':
        if 'hub.challenge' in req.GET:
            return HttpResponse(req.GET['hub.challenge'])
        else:
            print(dict(req.GET))
            for message in req.GET['entry.messaging']:
                print('yeah2')
                m = models.Message()
                m.sender = message['sender']
                m.text = message['message']['text']
                m.save()
    else:
        return HttpResponse('Sorry, bad token')

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
