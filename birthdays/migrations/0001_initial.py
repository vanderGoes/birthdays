# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore
from django.contrib.postgres.operations import HStoreExtension


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        HStoreExtension(),
        migrations.CreateModel(
            name='GeneratedPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(db_index=True, max_length=128, null=True, blank=True)),
                ('last_name', models.CharField(db_index=True, max_length=128, null=True, blank=True)),
                ('full_name', models.CharField(db_index=True, max_length=256, null=True, blank=True)),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('props', django.contrib.postgres.fields.hstore.HStoreField()),
                ('source_one_id', models.PositiveIntegerField()),
                ('source_two_id', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(db_index=True, max_length=128, null=True, blank=True)),
                ('last_name', models.CharField(db_index=True, max_length=128, null=True, blank=True)),
                ('full_name', models.CharField(db_index=True, max_length=256, null=True, blank=True)),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('props', django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PersonSourceMockOne',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(db_index=True, max_length=128, null=True, blank=True)),
                ('last_name', models.CharField(db_index=True, max_length=128, null=True, blank=True)),
                ('full_name', models.CharField(db_index=True, max_length=256, null=True, blank=True)),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('props', django.contrib.postgres.fields.hstore.HStoreField()),
                ('master', models.ForeignKey(blank=True, to='birthdays.Person', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PersonSourceMockTwo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(db_index=True, max_length=128, null=True, blank=True)),
                ('last_name', models.CharField(db_index=True, max_length=128, null=True, blank=True)),
                ('full_name', models.CharField(db_index=True, max_length=256, null=True, blank=True)),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('props', django.contrib.postgres.fields.hstore.HStoreField()),
                ('master', models.ForeignKey(blank=True, to='birthdays.Person', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='generatedperson',
            name='master',
            field=models.ForeignKey(blank=True, to='birthdays.Person', null=True),
        ),
        migrations.AddField(
            model_name='generatedperson',
            name='source_one_type',
            field=models.ForeignKey(related_name='+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='generatedperson',
            name='source_two_type',
            field=models.ForeignKey(related_name='+', to='contenttypes.ContentType'),
        ),
    ]
