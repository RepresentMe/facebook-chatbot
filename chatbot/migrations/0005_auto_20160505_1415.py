# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-05 14:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0004_auto_20160505_1245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='user_id',
            new_name='user',
        )
    ]
