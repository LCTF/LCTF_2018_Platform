# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-21 13:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_challenges_show'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solves',
            name='chalid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Challenges'),
        ),
        migrations.AlterField(
            model_name='solves',
            name='teamid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Teams'),
        ),
        migrations.AlterField(
            model_name='wrong_keys',
            name='chal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Challenges'),
        ),
        migrations.AlterField(
            model_name='wrong_keys',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Teams'),
        ),
    ]
