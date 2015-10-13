# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ontology', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='date',
            name='frequency',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='date',
            name='slug',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='firstname',
            name='frequency',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='firstname',
            name='slug',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lastname',
            name='frequency',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='lastname',
            name='slug',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='year',
            name='frequency',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='year',
            name='slug',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
