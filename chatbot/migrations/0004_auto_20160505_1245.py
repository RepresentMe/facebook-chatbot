# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-05 12:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0003_auto_20160505_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='current_question',
            field=models.IntegerField(default=-1),
        ),
    ]
