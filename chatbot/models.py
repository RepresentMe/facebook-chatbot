from __future__ import unicode_literals

from django.db import models


class Message(models.Model):
    text = models.CharField(max_length=2000)
    sender = models.CharField(max_length=200)

    def __str__(self):
        return "%s: %s" % (self.sender, self.text)


class User(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    current_question = models.IntegerField(default=-1)
    state = models.IntegerField(default=0)

    represent_id = models.IntegerField(default=-1, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    username = models.CharField(max_length=256, null=True, blank=True)
    first_name = models.CharField(max_length=256, null=True, blank=True)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    password = models.CharField(max_length=256, null=True, blank=True)

    auth_token = models.CharField(max_length=50, null=True, blank=True)

    def get_headers(self):
        return {'Authorization': 'Token %s' % self.auth_token}

    def __str__(self):
        return "Id: %s" % (self.id,)


class Answer(models.Model):
    user_id = models.CharField(max_length=200)
    question_id = models.IntegerField()
    answer = models.CharField(max_length=400)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return "%s (%s) %s" % (self.user_id, self.question_id, self.answer)

# Create your models here.
