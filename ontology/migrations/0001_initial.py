# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sources', django.contrib.postgres.fields.ArrayField(default=list, null=True, base_field=models.CharField(max_length=255), size=None)),
                ('date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FirstName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sources', django.contrib.postgres.fields.ArrayField(default=list, null=True, base_field=models.CharField(max_length=255), size=None)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LastName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sources', django.contrib.postgres.fields.ArrayField(default=list, null=True, base_field=models.CharField(max_length=255), size=None)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sources', django.contrib.postgres.fields.ArrayField(default=list, null=True, base_field=models.CharField(max_length=255), size=None)),
                ('year', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
