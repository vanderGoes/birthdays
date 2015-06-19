from __future__ import unicode_literals, absolute_import, print_function, division
import six

import json
from datetime import datetime

from django.apps import apps as django_apps
from django.core.management.base import BaseCommand
from django.db import connections

from birthdays.models import Person, PersonSource
from ._actions import DecodeMappingAction


class Command(BaseCommand):
    """
    Command to merge sources into GeneratedPersons
    """

    @staticmethod
    def add_to_master(source_name):
        source_model = django_apps.get_model(app_label="birthdays", model_name=source_name)
        master_set = Person.objects.all()

        assert issubclass(source_model, PersonSource), "Specified source {} is not a subclass of Person".format(source_name)

        for person_source in source_model.objects.all():
            if (person_source.full_name or person_source.first_name and person_source.last_name) \
                    and person_source.birth_date:
                person_source.fill_full_name()  # assure presence of full name
                try:
                    master = master_set.object.get(full_name=person_source.full_name)
                except Person.DoesNotExist:
                    master = master_set.create(
                        first_name=person_source.first_name,
                        last_name=person_source.last_name,
                        full_name=person_source.full_name,
                        birth_date=person_source.birth_date,
                        props=person_source.props
                    )
                person_source.master = master
                person_source.save()

    @staticmethod
    def prep_dict_for_fields(dictionary, mapping, date_format):
        fields = {}
        for key, value in six.iteritems(dictionary):
            if key in mapping:
                key = mapping[key]
            if key == "birth_date" and value:
                value = datetime.strptime(value, date_format).date()
            fields[key] = value if value else None
        return fields

    @staticmethod
    def from_fixture(file_name, source_name, mapping, date_format):
        source_model = django_apps.get_model(app_label="birthdays", model_name=source_name)
        with open(file_name, "r") as fp:
            data = json.load(fp)
            assert isinstance(data, list), "Expected a list inside " + file_name
            assert isinstance(data[0]["fields"], dict), "Expected JSON Django serialized models as elements in " + file_name
            for instance in data:
                fields = Command.prep_dict_for_fields(instance["fields"], mapping, date_format)
                source_model.objects.create(
                    first_name=fields.pop("first_name", None),
                    last_name=fields.pop("last_name", None),
                    full_name=fields.pop("full_name", None),
                    birth_date=fields.pop("birth_date", None),
                    props=fields
                )

    @staticmethod
    def from_records(file_name, source_name, mapping, date_format):
        pass

    @staticmethod
    def from_csv(file_name, source_name, mapping, date_format):
        pass

    @staticmethod
    def from_mysql_table(table_name, source_name, mapping, date_format):
        source_model = django_apps.get_model(app_label="birthdays", model_name=source_name)
        cursor = connections["mysql"].cursor()
        cursor.execute("SELECT COUNT(*) FROM {}".format(table_name))
        count = cursor.fetchone()[0]
        batch_size = 1000
        batch_count = int(count / batch_size) + 1
        for index in range(0, batch_count):
            offset = index * batch_size
            cursor.execute("SELECT * FROM {} LIMIT {} OFFSET {}".format(table_name, batch_size, offset))
            desc = cursor.description
            records = [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
            for record in records:
                fields = Command.prep_dict_for_fields(record, mapping, date_format)
                source_model.objects.create(
                    first_name=fields.pop("first_name", None),
                    last_name=fields.pop("last_name", None),
                    full_name=fields.pop("full_name", None),
                    birth_date=fields.pop("birth_date", None),
                    props=fields
                )

    def add_arguments(self, parser):
        parser.add_argument('input_type', type=unicode)
        parser.add_argument('-f', '--file', type=unicode)
        parser.add_argument('-s', '--source', type=unicode)
        parser.add_argument('-a', '--add-to-master', action="store_true")
        parser.add_argument('-m', '--mapping', type=unicode, action=DecodeMappingAction, nargs="?", default={})
        parser.add_argument('-d', '--date-format', type=unicode, nargs="?", default="%d-%m-%Y")

    def handle(self, *args, **options):
        handler = getattr(self, options["input_type"])
        handler(options["file"], options["source"], options["mapping"], options["date_format"])
        if options["add_to_master"]:
            self.add_to_master(options["source"])
