# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-29 19:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0005_auto_20190219_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalquestionnaireresponse',
            name='is_completed',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='questionnaireresponse',
            name='is_completed',
            field=models.CharField(default='', max_length=50),
        ),
    ]
