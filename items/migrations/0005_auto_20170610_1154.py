# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-10 11:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='price',
        ),
        migrations.RemoveField(
            model_name='item',
            name='price_currency',
        ),
    ]
