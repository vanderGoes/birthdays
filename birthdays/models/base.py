from django.db import models
from django.contrib.postgres.fields import HStoreField


class PersonBase(models.Model):

    first_name = models.CharField(max_length=128, db_index=True, null=True, blank=True)
    last_name = models.CharField(max_length=128, db_index=True, null=True, blank=True)
    full_name = models.CharField(max_length=256, db_index=True, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    props = HStoreField()

    def save(self, *args, **kwargs):
        if self.first_name and self.last_name and not self.full_name:
            self.full_name = self.first_name + self.last_name
        super(PersonBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class PersonSource(PersonBase):

    master = models.ForeignKey("Person", null=True, blank=True)

    class Meta:
        abstract = True