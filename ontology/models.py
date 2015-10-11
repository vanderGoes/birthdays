from django.db import models
from django.contrib.postgres.fields import ArrayField


class OntologyItem(models.Model):
    sources = ArrayField(
        models.CharField(max_length=255)
    )

    class Meta:
        abstract = True


class LastName(OntologyItem):
    name = models.CharField(max_length=255)


class FirstName(OntologyItem):
    name = models.CharField(max_length=255)


class Date(OntologyItem):
    date = models.DateField()


class Day(OntologyItem):
    day = models.PositiveSmallIntegerField()


class Month(OntologyItem):
    month = models.PositiveSmallIntegerField()


class Year(OntologyItem):
    year = models.IntegerField()
