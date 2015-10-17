from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.conf import settings


class OntologyItem(models.Model):
    sources = ArrayField(
        models.CharField(max_length=255),
        null=True,
        default=list
    )
    frequency = models.PositiveIntegerField(null=True)
    slug = models.CharField(max_length=255, null=True, db_index=True)

    slug_attr = "name"

    def add_source(self, model):
        model_name = model._meta.model_name
        if model_name not in self.sources:
            self.sources.append(model_name)

    @staticmethod
    def create_slug(name):
        raise NotImplementedError("Base class for ontology item can't create slugs")

    @classmethod
    def create_uri(cls, value):
        view_name = "{}_view".format(cls._meta.model_name)
        view_url = reverse(view_name, kwargs={"slug": cls.create_slug(value)})
        return "{}{}".format(settings.BIRTHDAYS_DOMAIN, view_url)

    def clean(self):
        self.slug = self.create_slug(
            getattr(self, self.slug_attr)
        )

    class Meta:
        abstract = True


class LastName(OntologyItem):
    name = models.CharField(max_length=255, db_index=True)

    @staticmethod
    def create_slug(name):
        return slugify(name)


class FirstName(OntologyItem):
    name = models.CharField(max_length=255, db_index=True)

    @staticmethod
    def create_slug(name):
        return slugify(name)


class Date(OntologyItem):
    date = models.DateField(db_index=True)

    slug_attr = "date"

    @staticmethod
    def create_slug(date):
        return date.strftime("%m-%d-%Y")


class Year(OntologyItem):
    year = models.IntegerField(db_index=True)

    slug_attr = "year"

    @staticmethod
    def create_slug(year):
        return str(year)
