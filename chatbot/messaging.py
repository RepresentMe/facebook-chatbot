import requests, json, logging
from django.conf import settings
from models import *


def send_message(user, message):
    if settings.DEBUG:
        m = Message()
        m.sender = user.id
        m.text = "Answer: %s" % (message,)
        m.save()
    else:
        question_req = {
            'recipient': {
                'id': user.id
            },
            'message': {
                'text': message
            }
        }
        url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % settings.BOT_KEY
        response_msg = json.dumps(question_req)
        r = requests.post(url, headers={"Content-Type": "application/json"}, data=response_msg)
        logging.debug(r.text)


class States:
    idle = 0
    question_asked = 1
    email_asked = 2
    name_asked = 3


def is_exit(string):
    return string == '@'


def get_error_list(dct):
    return '\n'.join('%s: %s' % (a[0], ' '.join(a[1])) for a in dct.items())

