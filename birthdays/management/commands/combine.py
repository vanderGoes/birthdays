from __future__ import unicode_literals, absolute_import, print_function, division

from django.apps import apps as django_apps
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from birthdays.models import GeneratedPerson


class Command(BaseCommand):
    """
    Command to merge sources into GeneratedPersons
    """

    @staticmethod
    def clean_record(record):
        # check primary fields
        to_check = ["first_name", "last_name", "full_name", "birth_date"]
        for check in to_check:
            if check + "_x" in record:
                # dealing with doubles
                if not record[check + "_x"] and not record[check + "_y"]:
                    # ignore record if primary fields differ, otherwise use value
                    if record[check + "_x"] != record[check + "_y"]:
                        return {}
                    else:
                        record[check] = record[check + "_x"]
                # try to copy one to two
                elif record[check + "_x"]:
                    record[check] = record[check + "_x"]
                # try to copy two to one
                elif record[check + "_y"]:
                    record[check] = record[check + "_y"]
            elif not check in record:
                # primary field missing, discard record
                return {}
            # clean fields that have doubles
            del record[check + "_x"]
            del record[check + "_y"]
        # returning cleaned record
        return record

    @staticmethod
    def combine(source_one, source_two, keys):
        model_one = django_apps.get_model(app_label="birthdays", model_name=source_one)
        model_two = django_apps.get_model(app_label="birthdays", model_name=source_two)
        content_one = ContentType.objects.get_for_model(model_one)
        content_two = ContentType.objects.get_for_model(model_two)
        data_one = model_one.objects.get_data_frame()
        data_two = model_two.objects.get_data_frame()
        merged = data_one.merge(data_two, on=keys)

        results = []
        for merge in merged.to_dict(orient="records"):
            generated = Command.clean_record(merge)
            if not generated:
                continue
            pkx = generated.pop("pk_x")
            pky = generated.pop("pk_y")
            gp = GeneratedPerson(
                first_name=generated.pop("first_name", None),
                last_name=generated.pop("last_name", None),
                full_name=generated.pop("full_name", None),
                birth_date=generated.pop("birth_date", None),
                props=generated,
                source_one_id=pkx,
                source_one_type=content_one,
                source_two_id=pky,
                source_two_type=content_two
            )
            gp.fill_full_name()
            results.append(gp)

        if results:
            GeneratedPerson.objects.bulk_create(results)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
