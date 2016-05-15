from messaging import *
import random

from django.core.exceptions import ValidationError


def register_me(user, message):
    if user.represent_id == -1:
        send_message(user, 'Now I am gonna create an account for you on represent.me\n'
                           'Please, use this method only if you don\'t have an account there yet\n'
                           'Note, that you can interrupt process at any stage typing single char: @\n'
                           'Now, what is your email address?')
        user.state = States.email_asked
    else:
        send_message(user, 'You already have an account')


def email_write(user, message):
    if is_exit(message.text):
        send_message(user, 'Stopped registration')
        user.state = States.idle
        return
    user.email = message.text
    try:
        user.full_clean()
    except ValidationError as e:
        send_message(user, 'An error occurred\n%s' % get_error_list(e.message_dict))
        return
    send_message(user, 'Email written.'
                       'What is your name? Ex: John Snow')
    user.state = States.name_asked


def name_write(user, message):
    if is_exit(message.text):
        send_message(user, 'Stopped registration')
        user.state = States.idle
        return
    tokens = message.text.split()
    if len(tokens) < 2:
        send_message(user, 'Sorry, can you repeat your name?')
    else:
        user.first_name = tokens[0]
        user.last_name = tokens[1]
        try:
            user.full_clean()
        except ValidationError as e:
            send_message(user, 'An error occurred\n%s' % get_error_list(e.message_dict))
            return
        send_message(user, 'Name written.')
        register(user, message)


def register(user, message):
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    user.password = ''.join(random.choice(chars) for _ in range(8))
    user.username = user.email
    r = requests.post('%s/auth/register/' % (settings.REPRESENT_URL,), {
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "password": user.password
    })
    resp = json.loads(r.text)
    if r.status_code == 201:
        user.represent_id = int(resp['id'])
        send_message(user, 'Your account successfully created. \n User id: %s. \n'
                           'Providing account details will be avaliable soon' % (user.represent_id))
    else:
        send_message(user,
                     'An error occurred:\n%s' % get_error_list(resp))
    user.state = States.idle


def authenticate(user):
    r = requests.post('%s/auth/login/'% (settings.REPRESENT_URL,),
                      {'username': user.username, 'password': user.password})
    j = r.json()
    if 'auth_token' in j:
        user.auth_token = j['auth_token']
    else:
        send_message(user, 'An error occurred:%s' % get_error_list(j))


def authenticated(fun):
    def new_fun(user, message):
        if not user.auth_token:
            authenticate(user)
        fun(user, message)

    return new_fun
