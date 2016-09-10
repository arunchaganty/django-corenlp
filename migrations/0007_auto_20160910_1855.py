# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-10 18:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('corenlp', '0006_auto_20160907_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Keeps track of when this sentence was added'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Keeps track of when this sentence was added'),
        ),
        migrations.AlterField(
            model_name='mention',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Keeps track of when this sentence was added'),
        ),
        migrations.AlterField(
            model_name='relation',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Keeps track of when this sentence was added'),
        ),
        migrations.AlterField(
            model_name='sentence',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Keeps track of when this sentence was added'),
        ),
    ]
