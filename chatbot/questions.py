import requests, json
from django.conf import settings
import logging
import models
import auth


def process_message(user_id, message):
    m = models.Message()
    m.sender = user_id
    m.text = message
    user = models.User.objects.get_or_create(pk=m.sender)
    user = user[0]
    m.save()
    user.save()
    states_dict[user.state](user, m)


def send_message(user_id, message):
    if settings.DEBUG:
        m = models.Message()
        m.sender = user_id
        m.text = "Answer: %s" % (message,)
        m.save()
    else:
        question_req = {
            'recipient': {
                'id': user_id
            },
            'message': {
                'text': message
            }
        }
        url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % settings.BOT_KEY
        response_msg = json.dumps(question_req)
        r = requests.post(url, headers={"Content-Type": "application/json"}, data=response_msg)
        logging.debug(r.text)


def idle(user, message):
    if message.text.lower() == 'ask':
        ask_question(user, message)
    else:
        misunderstood(user, message)


def ask_question(user, message):
    l = models.Answer.objects.filter(user_id=user.id).values('question_id').distinct()
    l = ",".join(list(map(lambda a: str(a['question_id']), l)))
    if len(l) > 1:
        l = "?&id__in!=" + l
    else:
        l = ""
    quest = requests.get('https://represent.me/api/next_question/%s' % l)
    quest = json.loads(quest.text)['results'][0]
    user.current_question = quest['id']
    user.state = States.question_asked[0]
    user.save()
    send_message(user.id, quest['question'])


def misunderstood(user, message):
    send_message(user.id, 'Sorry, I didn\'t understand you :(. If you want me to ask question, type "Ask"')


def write_answer(user, message):
    a = models.Answer()
    a.user_id = user.id
    a.question_id = user.current_question
    a.answer = message.text
    a.save()
    user.current_question = -1
    user.save()
    send_message(user.id, "Answer written")


states_dict = {}


class States:
    idle = (0, idle)
    question_asked = (1, write_answer)


for p in States.__dict__.items():
    if p[0][0] != '_':
        states_dict[p[1][0]] = p[1][1]