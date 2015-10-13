from __future__ import unicode_literals

import string

from pandas import DataFrame

from django.db import models
from django.contrib.postgres.fields import HStoreField
from django.core.urlresolvers import reverse
from django.conf import settings

from polymorphic import PolymorphicModel, PolymorphicManager


class PersonManager(PolymorphicManager):

    def get_data_frame(self, *args, **kwargs):
        people = super(PersonManager, self).get_queryset(*args, **kwargs)
        data = [
            dict(
                person.props,
                first_name=person.first_name,
                initials=person.initials,
                prefix=person.prefix,
                last_name=person.last_name,
                full_name=person.full_name,
                birth_date=person.birth_date,
                pk=person.pk
            ) for person in people
        ]
        if data:
            columns = ["first_name", "last_name", "full_name", "birth_date", "pk"] + people[0].props.keys()
            return DataFrame(data, columns=columns)
        else:
            return None


class PersonMixin(object):

    prefixes = [
        "af",
        "aan",
        "bij",
        "de", "den", "der", "d'",
        "het", "'t",
        "in",
        "onder",
        "op",
        "over",
        "'s",
        "'t",
        "te", "ten", "ter",
        "tot",
        "uit", "uijt",
        "van", "vanden",
        "ver",
        "voor",
        "a",
        "al",
        "am",
        "auf",
        "aus",
        "ben", "bin",
        "da",
        "dal", "dalla", "della",
        "das", "die", "den", "der", "des",
        "deca",
        "degli",
        "dei",
        "del",
        "di",
        "do",
        "don",
        "dos",
        "du",
        "el",
        "i",
        "im",
        "L",
        "la", "las",
        "le", "les",
        "lo", "los",
        "o'",
        "tho", "thoe", "thor", "to", "toe",
        "unter",
        "vom", "von",
        "vor",
        "zu", "zum", "zur",
    ]

    def fill_full_name(self):
        if self.first_name and self.last_name and not self.full_name:
            self.full_name = "{} {}".format(self.first_name, self.last_name)

    def split_full_name(self):
        if not self.full_name or (self.first_name and self.last_name):
            return
        names = self.full_name.lower().split(" ")
        if not len(names) > 1:
            return

        last_name = names.pop()
        first_names = []
        prefixes = []
        for name in names:
            if name in self.prefixes:
                prefixes.append(name)
            else:
                first_names.append(name)

        self.prefix = " ".join(prefixes) if prefixes else None
        self.last_name = "{} {}".format(self.prefix, last_name.capitalize()) if self.prefix else last_name.capitalize()
        self.first_name = " ".join(map(string.capitalize, first_names))

    def __unicode__(self):
        return "{} {}".format(self.__class__.__name__, self.id)


class Person(PersonMixin, models.Model):

    first_name = models.CharField(max_length=128, db_index=True, null=True, blank=True)
    initials = models.CharField(max_length=20, db_index=True, null=True, blank=True)
    prefix = models.CharField(max_length=20, db_index=True, null=True, blank=True)
    last_name = models.CharField(max_length=128, db_index=True, null=True, blank=True)
    full_name = models.CharField(max_length=256, db_index=True, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    props = HStoreField()

    def save(self, *args, **kwargs):
        if self.first_name and self.last_name and not self.full_name:
            self.fill_full_name()
        if self.full_name and (not self.first_name or not self.last_name):
            self.split_full_name()
        super(Person, self).save(*args, **kwargs)


class PersonSource(PersonMixin, PolymorphicModel):

    objects = PersonManager()

    first_name = models.CharField(max_length=128, db_index=True, null=True, blank=True)
    initials = models.CharField(max_length=20, db_index=True, null=True, blank=True)
    prefix = models.CharField(max_length=20, db_index=True, null=True, blank=True)
    last_name = models.CharField(max_length=128, db_index=True, null=True, blank=True)
    full_name = models.CharField(max_length=256, db_index=True, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    props = HStoreField()
    master = models.ForeignKey(Person, null=True, blank=True, related_name="sources")

    def save(self, *args, **kwargs):
        self.fill_full_name()
        self.split_full_name()
        super(PersonSource, self).save(*args, **kwargs)

    def get_uri(self):
        admin_view_name = "admin:birthdays_{}_change".format(self._meta.model_name)
        admin_url = reverse(admin_view_name, args=(self.id,))
        return "{}{}".format(settings.BIRTHDAYS_DOMAIN, admin_url)
