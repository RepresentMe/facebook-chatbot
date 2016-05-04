from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from . import models


def webhook(req):
    if 'hub.verify_token' in req.GET and req.GET['hub.verify_token'] == 'test':
        return HttpResponse(req.GET['hub.challenge'])
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
