# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-29 21:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('corenlp', '0009_auto_20160922_0059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, help_text='Keeps track of when this sentence was added')),
                ('score', models.FloatField(help_text='Linking score for the best entity match', null=True)),
                ('entity', models.ForeignKey(help_text='Entity participating in link', on_delete=django.db.models.deletion.CASCADE, to='corenlp.Entity')),
            ],
        ),
        migrations.RemoveField(
            model_name='mention',
            name='alt_entity',
        ),
        migrations.RemoveField(
            model_name='mention',
            name='alt_entity_score',
        ),
        migrations.RemoveField(
            model_name='mention',
            name='best_entity',
        ),
        migrations.RemoveField(
            model_name='mention',
            name='best_entity_score',
        ),
        migrations.RemoveField(
            model_name='mention',
            name='canonical_gloss',
        ),
        migrations.RemoveField(
            model_name='mention',
            name='doc_canonical_char_begin',
        ),
        migrations.RemoveField(
            model_name='mention',
            name='doc_canonical_char_end',
        ),
        migrations.RemoveField(
            model_name='mention',
            name='unambiguous_link',
        ),
        migrations.AddField(
            model_name='link',
            name='mention',
            field=models.OneToOneField(help_text='Mention participating in link', on_delete=django.db.models.deletion.CASCADE, to='corenlp.Mention'),
        ),
    ]