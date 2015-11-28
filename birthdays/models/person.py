from __future__ import unicode_literals
import six

import string

from pandas import DataFrame

from django.db import models
from django.contrib.postgres.fields import HStoreField
from django.core.urlresolvers import reverse
from django.conf import settings

from polymorphic import PolymorphicModel, PolymorphicManager

from ontology.models import (
    LastName,
    FirstName,
    Date,
    Year
)


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

    @classmethod
    def register_from_fields(cls, fields, source_model):
        person_source = source_model(
            first_name=fields.pop("first_name", None),
            initials=fields.pop("initials", None),
            prefix=fields.pop("prefix", None),
            last_name=fields.pop("last_name", None),
            full_name=fields.pop("full_name", None),
            birth_date=fields.pop("birth_date", None),
            props=fields
        )

        for attr in ["first_name", "initials", "prefix", "last_name", "full_name"]:
            value = getattr(person_source, attr, None)
            if value is not None and isinstance(value, six.string_types):
                setattr(person_source, attr, value.strip())

        person_source.clean()
        person_source.save()

        if person_source.last_name:
            last_name, created = LastName.objects.get_or_create(name=person_source.last_name)
            last_name.frequency = 1 if created or last_name.frequency is None else last_name.frequency + 1
            last_name.add_source(source_model)
            last_name.clean()
            last_name.save()
        if person_source.first_name:
            first_name, created = FirstName.objects.get_or_create(name=person_source.first_name)
            first_name.frequency = 1 if created or first_name.frequency is None else first_name.frequency + 1
            first_name.add_source(source_model)
            first_name.clean()
            first_name.save()
        if person_source.birth_date:
            date, created = Date.objects.get_or_create(date=person_source.birth_date)
            date.frequency = 1 if created or date.frequency is None else date.frequency + 1
            date.add_source(source_model)
            date.clean()
            date.save()
            year, created = Year.objects.get_or_create(year=person_source.birth_date.year)
            year.frequency = 1 if created or year.frequency is None else year.frequency + 1
            year.add_source(source_model)
            year.clean()
            year.save()

        return person_source


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

    def fill_full_name(self, force=False):
        if (self.first_name and self.last_name and not self.full_name) or force:
            if not self.prefix:
                self.full_name = "{} {}".format(self.first_name, self.last_name)
            else:
                self.full_name = "{} {} {}".format(self.first_name, self.prefix, self.last_name)

    def split_full_name(self, force=False):
        if (not self.full_name or (self.first_name and self.last_name)) or force:
            return
        names = self.full_name.lower().split(" ")
        if not len(names) > 1:
            return

        # last_name = names.pop()
        # first_names = []
        # prefixes = []
        # for name in names:
        #     if name in self.prefixes:
        #         prefixes.append(name)
        #     else:
        #         first_names.append(name)

		if len(names)==2:
			first_name = names(0)
			last_name = names(1)
		else:
			#prefix check
			for name in names:
				if name in self.prefixes:
					pos_prefix = pos_prefix.append(names.index(name))
			#split with prefix
			if pos_prefix(0)!=null:
				if pos_prefix(0)==1:
					first_name = names[:1]
					last_name = names[1:]
				else:
					for i in range(0,pos_prefix(0)-1):
						first_name_temp = names[:pos_prefix(0)-i]
						last_name_temp = names[pos_prefix(0)-i:]
							if list_juice(last_name_temp)==true:
								first_name=first_name_temp.capitalize()
								last_name=last_name_temp.capitalize()
			#split without prefix
			else:
				for i in range(1, len(names)):
					first_name_temp = names[:len(names)-i]
					last_name_temp = names[len(names)-i:]
					if list_juice(last_name_temp)==true:
						first_name=first_name_temp.capitalize()
						last_name=last_name_temp.capitalize()
		pos_prefix=[]

        self.prefix = " ".join(prefixes) if prefixes else None
        self.last_name = "{} {}".format(self.prefix, last_name.capitalize()) if self.prefix else last_name.capitalize()
        self.first_name = " ".join(map(string.capitalize, first_names))

    @staticmethod
    def list_juice(last_name_check):
		query_set = Person.objects \
		.filter(
				first_name__isnull=False,
				last_name__isnull=False,
				last_name=last_name_check
			) \
			.exist()
		return #boolean

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
        if self.first_name and self.last_name and not self.full_name:
            self.fill_full_name()
        if self.full_name and (not self.first_name or not self.last_name):
            self.split_full_name()
        super(PersonSource, self).save(*args, **kwargs)

    def get_uri(self):
        admin_view_name = "admin:birthdays_{}_change".format(self._meta.model_name)
        admin_url = reverse(admin_view_name, args=(self.id,))
        return "{}{}".format(settings.BIRTHDAYS_DOMAIN, admin_url)
