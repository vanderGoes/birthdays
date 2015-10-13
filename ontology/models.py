from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify


class OntologyItem(models.Model):
    sources = ArrayField(
        models.CharField(max_length=255),
        null=True,
        default=list
    )
    frequency = models.PositiveIntegerField(null=True)
    slug = models.CharField(max_length=255, null=True)

    def add_source(self, model):
        model_name = model._meta.model_name
        if model_name not in self.sources:
            self.sources.append(model_name)

    def create_slug(self):
        raise NotImplementedError("Base class for ontology item can't create slugs")

    def clean(self):
        self.slug = self.create_slug()

    class Meta:
        abstract = True


class LastName(OntologyItem):
    name = models.CharField(max_length=255)

    def create_slug(self):
        return slugify(self.name)


class FirstName(OntologyItem):
    name = models.CharField(max_length=255)

    def create_slug(self):
        return slugify(self.name)


class Date(OntologyItem):
    date = models.DateField()

    def create_slug(self):
        return self.date.strftime("%m-%d-%Y")


class Year(OntologyItem):
    year = models.IntegerField()

    def create_slug(self):
        return str(self.year)
