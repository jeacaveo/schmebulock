# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-17 20:38
from __future__ import unicode_literals

import audit_log.models.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cities', '0010_adjust_unique_attributes'),
        ('items', '0009_auto_20170611_2307'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_with_session_key', audit_log.models.fields.CreatingSessionKeyField(editable=False, max_length=40, null=True)),
                ('modified_with_session_key', audit_log.models.fields.LastSessionKeyField(editable=False, max_length=40, null=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('address', models.CharField(max_length=256)),
                ('created_by', audit_log.models.fields.CreatingUserField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_items_location_set', to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_district', to='cities.District')),
                ('modified_by', audit_log.models.fields.LastUserField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_items_location_set', to=settings.AUTH_USER_MODEL, verbose_name='modified by')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
