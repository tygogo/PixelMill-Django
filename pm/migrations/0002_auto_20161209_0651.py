# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-09 06:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile',
            field=models.TextField(max_length=32, null=True, verbose_name='简介'),
        ),
    ]
