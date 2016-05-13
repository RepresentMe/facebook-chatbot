import auth

from chatbot.messaging import *


def process_message(user_id, message):
    m = Message()
    m.sender = user_id
    m.text = message
    user = User.objects.get_or_create(pk=m.sender)
    user = user[0]
    m.save()
    user.save()
    states_dict[user.state](user, m)
    user.save()


def idle(user, message):
    cmd = message.text.lower()
    if cmd == 'ask':
        ask_question(user, message)
    elif cmd == 'help':
        help(user, message)
    elif cmd == 'reg':
        auth.register_me(user, message)
    elif cmd == 'register':
        auth.register(user, message)
    else:
        misunderstood(user, message)


def ask_question(user, message):
    l = Answer.objects.filter(user_id=user.id).values('question_id').distinct()
    l = ",".join(list(map(lambda a: str(a['question_id']), l)))
    if len(l) > 1:
        l = "?&id__in!=" + l
    else:
        l = ""
    quest = requests.get('https://represent.me/api/next_question/%s' % l)
    quest = json.loads(quest.text)['results'][0]
    user.current_question = quest['id']
    user.state = States.question_asked
    user.save()
    send_message(user, quest['question'])


def misunderstood(user, message):
    send_message(user, 'Sorry, I didn\'t understand you :(. If you want me to ask question, type "Ask"')


def help(user, message):
    pass


def write_answer(user, message):
    a = Answer()
    a.user_id = user.id
    a.question_id = user.current_question
    a.answer = message.text
    a.save()
    user.current_question = -1
    user.state = States.idle
    user.save()
    send_message(user, "Answer written")


states_dict = {
    States.idle: idle,
    States.question_asked: write_answer,
    States.email_asked: auth.email_write,
    States.name_asked: auth.name_write
}
