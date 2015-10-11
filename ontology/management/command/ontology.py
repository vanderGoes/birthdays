from __future__ import unicode_literals, absolute_import, print_function, division

from django.apps import apps as django_apps
from django.core.management.base import BaseCommand

from birthdays.models import PersonSource
from ontology.models import LastName, FirstName, Date, Year


class Command(BaseCommand):
    """
    Command to created canonic entities
    """

    @staticmethod
    def add_to_ontology(source_model):
        for last_name in source_model.objects.values_list("last_name", flat=True).distinct():
            if not last_name:
                continue
            last_name_record, created = LastName.objects.get_or_create(
                name=last_name
            )
            last_name_record.add_source(source_model)
            last_name_record.save()
        for first_name in source_model.objects.values_list("first_name", flat=True).distinct():
            if not first_name:
                continue
            first_name_record, created = FirstName.objects.get_or_create(
                name=first_name
            )
            first_name_record.add_source(source_model)
            first_name_record.save()
        for birth_date in source_model.objects.values_list("birth_date", flat=True).distinct():
            if not birth_date:
                continue
            date_record, created = Date.objects.get_or_create(
                date=birth_date
            )
            date_record.add_source(source_model)
            date_record.save()
            year_record, created = Year.objects.get_or_create(
                year=birth_date.year
            )
            year_record.add_source(source_model)
            year_record.save()

    def add_arguments(self, parser):
        parser.add_argument(
            'extend_type',
            type=unicode,
            help="The extend method. Either 'add_to_master' or 'extend_master'."
        )
        parser.add_argument(
            '-s', '--source',
            type=unicode,
            help="The source to add or extend from."
        )

    def handle(self, *args, **options):
        source_model = django_apps.get_model(app_label="birthdays", model_name=options["source"])
        assert issubclass(source_model, PersonSource), "Specified source {} is not a subclass of PersonSource".format(options["source"])
        handler = getattr(self, options["extend_type"])
        handler(source_model)
