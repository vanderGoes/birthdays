from django.db import models
from django.contrib.postgres.fields import HStoreField

from pandas import DataFrame


class PersonManager(models.Manager):

    def get_data_frame(self, *args, **kwargs):
        people = super(PersonManager, self).get_queryset(*args, **kwargs)
        data = [
            dict(
                person.props,
                first_name=person.first_name,
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


class PersonBase(models.Model):

    objects = PersonManager()

    first_name = models.CharField(max_length=128, db_index=True, null=True, blank=True)
    last_name = models.CharField(max_length=128, db_index=True, null=True, blank=True)
    full_name = models.CharField(max_length=256, db_index=True, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    props = HStoreField()

    def fill_full_name(self):
        if self.first_name and self.last_name and not self.full_name:
            self.full_name = self.first_name + self.last_name

    def save(self, *args, **kwargs):
        self.fill_full_name()
        super(PersonBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class PersonSource(PersonBase):

    master = models.ForeignKey("Person", null=True, blank=True)

    class Meta:
        abstract = True