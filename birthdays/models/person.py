from pandas import DataFrame

from django.db import models
from django.contrib.postgres.fields import HStoreField

from polymorphic import PolymorphicModel


class PersonManager(models.Manager):

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

    def fill_full_name(self):
        self.full_name = "{} {}".format(self.first_name, self.last_name)

    def split_full_name(self):
        pass  # depends heavily on the source

    def __unicode__(self):
        return "{} {}".format(self.__class__.__name__, self.id)


class Person(PersonMixin, models.Model):

    objects = PersonManager()

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
        if self.first_name and self.last_name and not self.full_name:
            self.fill_full_name()
        if self.full_name and (not self.first_name or not self.last_name):
            self.split_full_name()
        super(PersonSource, self).save(*args, **kwargs)

