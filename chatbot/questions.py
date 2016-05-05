import requests, json
from django.conf import settings
import logging


def ask_question(user_id):
    quest = requests.get('https://represent.me/api/next_question/')
    ret_string = json.loads(quest.text)['results'][0]['question']
    question_req = {
        'recipient': {
            'id': user_id
        },
        'message': {
            'text': ret_string
        }
    }
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % settings.BOT_KEY
    response_msg = json.dumps(question_req)
    r = requests.post(url, headers={"Content-Type": "application/json"}, data=response_msg)
    logging.debug(r.text)


def misunderstood(user_id):
    question_req = {
        'recipient': {
            'id': user_id
        },
        'message': {
            'text': 'Sorry, I didn\'t understand you :(. If you want me to ask question, type "Ask"'
        }
    }
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % settings.BOT_KEY
    response_msg = json.dumps(question_req)
    r = requests.post(url, headers={"Content-Type": "application/json"}, data=response_msg)
    logging.debug(r.text)
