from __future__ import unicode_literals, absolute_import, print_function, division

from django.core.management.base import BaseCommand
from django.db.models import Count

from birthdays.models import Person
from birthdays.helpers import output_person


class Command(BaseCommand):
    """
    Command to list all the people we have more information on than average.
    """

    @staticmethod
    def list_juice():
        query_set = Person.objects \
            .annotate(source_num=Count("sources")) \
            .all() \
            .order_by("-source_num")
        for person in query_set[:100]:
            output_person(person)

    def handle(self, *args, **options):
        self.list_juice()
