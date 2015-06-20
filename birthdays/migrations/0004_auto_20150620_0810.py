# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('birthdays', '0003_phonebooksource'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='initials',
            field=models.CharField(db_index=True, max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='prefix',
            field=models.CharField(db_index=True, max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='personsource',
            name='initials',
            field=models.CharField(db_index=True, max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='personsource',
            name='prefix',
            field=models.CharField(db_index=True, max_length=20, null=True, blank=True),
        ),
    ]
