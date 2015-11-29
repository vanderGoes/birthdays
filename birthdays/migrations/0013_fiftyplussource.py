# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('birthdays', '0012_knacsource_musicsocietysource_triathlonsource'),
    ]

    operations = [
        migrations.CreateModel(
            name='FiftyPlusSource',
            fields=[
                ('personsource_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='birthdays.PersonSource')),
            ],
            options={
                'abstract': False,
            },
            bases=('birthdays.personsource',),
        ),
    ]
