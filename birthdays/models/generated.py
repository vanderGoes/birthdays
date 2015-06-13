from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .base import PersonSource


class GeneratedPerson(PersonSource):

    source_one = GenericForeignKey(ct_field="source_one_type", fk_field="source_one_id")
    source_one_type = models.ForeignKey(ContentType)
    source_one_id = models.PositiveIntegerField()
    source_two = GenericForeignKey(ct_field="source_two_type", fk_field="source_two_id")
    source_two_type = models.ForeignKey(ContentType)
    source_two_id = models.PositiveIntegerField()
