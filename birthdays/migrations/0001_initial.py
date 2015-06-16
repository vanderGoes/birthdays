# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore
import birthdays.models.person


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
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
            bases=(birthdays.models.person.PersonMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PersonSource',
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
            bases=(birthdays.models.person.PersonMixin, models.Model),
        ),
        migrations.CreateModel(
            name='GeneratedPerson',
            fields=[
                ('personsource_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='birthdays.PersonSource')),
            ],
            options={
                'abstract': False,
            },
            bases=('birthdays.personsource',),
        ),
        migrations.CreateModel(
            name='PersonSourceMockOne',
            fields=[
                ('personsource_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='birthdays.PersonSource')),
            ],
            options={
                'abstract': False,
            },
            bases=('birthdays.personsource',),
        ),
        migrations.CreateModel(
            name='PersonSourceMockThree',
            fields=[
                ('personsource_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='birthdays.PersonSource')),
            ],
            options={
                'abstract': False,
            },
            bases=('birthdays.personsource',),
        ),
        migrations.CreateModel(
            name='PersonSourceMockTwo',
            fields=[
                ('personsource_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='birthdays.PersonSource')),
            ],
            options={
                'abstract': False,
            },
            bases=('birthdays.personsource',),
        ),
        migrations.AddField(
            model_name='personsource',
            name='master',
            field=models.ForeignKey(related_name='sources', blank=True, to='birthdays.Person', null=True),
        ),
        migrations.AddField(
            model_name='personsource',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_birthdays.personsource_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='generatedperson',
            name='source_one',
            field=models.ForeignKey(related_name='primary_set', to='birthdays.PersonSource'),
        ),
        migrations.AddField(
            model_name='generatedperson',
            name='source_two',
            field=models.ForeignKey(related_name='secondary_set', to='birthdays.PersonSource'),
        ),
    ]
