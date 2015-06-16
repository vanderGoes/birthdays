from django.db import models

from .person import PersonSource


class GeneratedPerson(PersonSource):

    source_one = models.ForeignKey(PersonSource, related_name="primary_set")
    source_two = models.ForeignKey(PersonSource, related_name="secondary_set")
