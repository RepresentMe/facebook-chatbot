from __future__ import unicode_literals

from django.db import models


class Message(models.Model):
    text = models.CharField(max_length=2000)
    sender = models.CharField(max_length=200)


class User(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    current_question = models.IntegerField(default=-1)


class Answer(models.Model):
    user = models.ForeignKey(User)
    question_id = models.IntegerField()
    answer = models.CharField(max_length=400)

# Create your models here.
