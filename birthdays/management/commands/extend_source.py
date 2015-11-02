from __future__ import unicode_literals, absolute_import, print_function, division
import six

import json
from datetime import datetime

from django.apps import apps as django_apps
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.models import Q

from birthdays.models import Person, PersonSource
from ._actions import DecodeMappingAction


class Command(BaseCommand):
    """
    Command to merge sources into GeneratedPersons
    """

    @staticmethod
    def add_to_master(source_model):
        master_set = Person.objects.all()

        for person_source in source_model.objects.all():
            if person_source.full_name and person_source.birth_date:
                try:
                    master = master_set.get(full_name=person_source.full_name, birth_date=person_source.birth_date)
                except Person.DoesNotExist:
                    master = master_set.create(
                        first_name=person_source.first_name,
                        initials=person_source.initials,
                        prefix=person_source.prefix,
                        last_name=person_source.last_name,
                        full_name=person_source.full_name,
                        birth_date=person_source.birth_date,
                        props=person_source.props
                    )
                person_source.master = master
                person_source.save()

    @staticmethod
    def extend_master(source_model):
        master_set = Person.objects.all()
        for person_source in source_model.objects.all():
            try:
                master = master_set.get(full_name=person_source.full_name)
            except Person.DoesNotExist:
                continue
            master.props.update(person_source.props)
            master.save()
            person_source.master = master
            person_source.save()

    @staticmethod
    def split_full_name(source_model):
        for person_source in source_model.objects.all():
            person_source.split_full_name()
            person_source.save()

    @staticmethod
    def correct_last_names(source_model):
        query_set = source_model.objects.filter(
            prefix__isnull=False,
            full_name__isnull=False,
            last_name__isnull=False,
        ).exclude(
            prefix="",
            full_name="",
            last_name="",
        )
        for person_source in query_set:
            prefix_sample = person_source.prefix.split(" ")[0]
            if prefix_sample not in person_source.last_name:
                print("Fixing: ", person_source.last_name, " with prefix ", person_source.prefix, " -> ", person_source.id)
                person_source.last_name = "{} {}".format(
                    person_source.prefix.strip(),
                    person_source.last_name.strip()
                )
                person_source.save()
                print("Fixed with: ", person_source.last_name)

    @staticmethod
    def strip_name_whitespace(source_model):
        name_attrs = ["first_name", "last_name", "full_name"]
        for attr in name_attrs:
            startswith_filter = "{}__startswith".format(attr)
            endswith_filter = "{}__endswith".format(attr)
            for person in PersonSource.objects.filter(
                    Q(**{startswith_filter: " "}) | Q(**{endswith_filter: " "})):
                value = getattr(person, attr)
                setattr(person, attr, value.strip())
                person.save()

    def add_arguments(self, parser):
        parser.add_argument(
            'extend_type',
            type=unicode,
            help="The extend method. Either 'add_to_master', 'split_full_name' or 'extend_master'."
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

