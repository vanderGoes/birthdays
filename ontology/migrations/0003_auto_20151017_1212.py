# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ontology', '0002_auto_20151013_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='firstname',
            name='name',
            field=models.CharField(max_length=255, db_index=True),
        ),
        migrations.AlterField(
            model_name='lastname',
            name='name',
            field=models.CharField(max_length=255, db_index=True),
        ),
        migrations.AlterField(
            model_name='year',
            name='year',
            field=models.IntegerField(db_index=True),
        ),
    ]
