from django.db import models
from django.contrib.postgres.fields import ArrayField


class OntologyItem(models.Model):
    sources = ArrayField(
        models.CharField(max_length=255),
        null=True,
        default=list
    )

    def add_source(self, model):
        model_name = model._meta.model_name
        if model_name not in self.sources:
            self.sources.append(model_name)

    class Meta:
        abstract = True


class LastName(OntologyItem):
    name = models.CharField(max_length=255)


class FirstName(OntologyItem):
    name = models.CharField(max_length=255)


class Date(OntologyItem):
    date = models.DateField()


class Year(OntologyItem):
    year = models.IntegerField()
