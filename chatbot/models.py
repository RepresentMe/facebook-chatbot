from __future__ import unicode_literals

from django.db import models


class Message(models.Model):
    text = models.CharField(max_length=2000)
    sender = models.CharField(max_length=200)


class User(models.Model):
    id = models.CharField(max_length=300, primary_key=True)
    current_question = models.CharField(max_length=200)
# Create your models here.
