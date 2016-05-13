from messaging import *
import random


def register_me(user, message):
    send_message(user, 'Now I am gonna create an account for you on represent.me\n'
                       'Please, use this method only if you don\'t have an account there yet\n'
                       'Note, that you can interrupt process at any stage typing single char: @\n'
                       'Now, what is your email address?')
    user.state = States.email_asked


def email_write(user, message):
    user.email = message.text
    send_message(user, 'Email written.'
                       'What is your name? Ex: John Snow')
    user.state = States.name_asked


def name_write(user, message):
    tokens = message.text.split()
    if len(tokens) < 2:
        send_message(user, 'Sorry, can you repeat your name?')
    else:
        user.firstname = tokens[0]
        user.lastname = tokens[1]
        send_message(user, 'Name written.')
        user.state = States.idle


def register(user, message):
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    user.password = ''.join(random.choice(chars) for _ in range(8))
    user.username = user.email
    r = requests.post('https://test.represent.me/auth/register/', {
        "email": user.email,
        "username": user.username,
        "first_name": user.firstname,
        "last_name": user.lastname,
        "password": user.password
    })
    pass
