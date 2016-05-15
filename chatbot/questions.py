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
    quest = requests.get('%s/api/next_question/%s' % (settings.REPRESENT_URL, l))
    quest = json.loads(quest.text)['results'][0]
    user.current_question = quest['id']
    user.state = States.question_asked
    user.save()
    send_message(user,
                 '%s\nType your attitude to this question from -2 (Strongly disagree) to 2 (Strongly agree)' % quest[
                     'question'])


def misunderstood(user, message):
    send_message(user, 'Sorry, I didn\'t understand you :(. To get help type "Help"')


help_text = open('docs/help.txt').read()


def help(user, message):
    send_message(user, help_text)


def write_answer(user, message):
    if is_exit(message.text):
        send_message(user, 'Answering canceled')
        user.state = States.idle
        return
    try:
        ans = int(message.text)
        if ans not in range(-2, 3):
            raise Exception
    except:
        send_message(user, 'Your answer not a single number between -2 and 2')
        return
    a = Answer()
    a.user_id = user.id
    a.question_id = user.current_question
    a.answer = message.text
    a.sent = send_message(user, message)
    a.save()
    user.current_question = -1
    user.state = States.idle
    user.save()
    send_message(user, "Answer written")


@auth.authenticated
def send_answers(user, message):
    r = requests.post('%s/api/question_votes/' % (settings.REPRESENT_URL,), {
        'object_id': user.current_question,
        'value': message.text
    }, headers=user.get_headers())
    return r.status_code // 100 == 4


states_dict = {
    States.idle: idle,
    States.question_asked: write_answer,
    States.email_asked: auth.email_write,
    States.name_asked: auth.name_write
}
