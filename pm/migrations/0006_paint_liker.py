# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-31 14:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pm', '0005_auto_20161231_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='paint',
            name='liker',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
