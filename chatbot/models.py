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

    def __str__(self):
        return "Id: %s" % (self.id,)


class Answer(models.Model):
    user_id = models.CharField(max_length=200)
    question_id = models.IntegerField()
    answer = models.CharField(max_length=400)

    def __str__(self):
        return "%s (%s) %s" % (self.user_id, self.question_id, self.answer)

# Create your models here.
