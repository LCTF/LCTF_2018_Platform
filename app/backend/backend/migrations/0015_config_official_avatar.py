# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-30 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='official_avatar',
            field=models.ImageField(default='avatar/logi-mini.png', upload_to='avatar'),
            preserve_default=False,
        ),
    ]
