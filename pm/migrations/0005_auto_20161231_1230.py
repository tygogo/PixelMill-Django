# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-31 12:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0004_auto_20161230_0352'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=128, verbose_name='标题')),
                ('desc', models.TextField(max_length=128, verbose_name='描述')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('days', models.IntegerField(default=7)),
            ],
        ),
        migrations.CreateModel(
            name='ChallengeShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField(default=0)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pm.Challenge')),
                ('paint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pm.Paint')),
            ],
        ),
        migrations.AddField(
            model_name='challenge',
            name='paints',
            field=models.ManyToManyField(through='pm.ChallengeShip', to='pm.Paint'),
        ),
    ]
