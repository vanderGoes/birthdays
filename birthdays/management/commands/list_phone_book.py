from __future__ import unicode_literals, absolute_import, print_function, division

from django.core.management.base import BaseCommand

from birthdays.models import PhoneBookSource, WieOWieSource, PersonSource


class Command(BaseCommand):
    """
    Command to list all the people we have more information on than average.
    """

    @staticmethod
    def list_phone_book():
        query_set = PersonSource.objects \
            .not_instance_of(PhoneBookSource, WieOWieSource) \
            .filter(props__has_key="city")[:100]
        for person in query_set:
            full_name = person.full_name
            birth_date = person.birth_date
            last_name = person.last_name
            city = person.props["city"]
            if not city:
                continue
            city = city.lower().capitalize()
            phonebook_set = PhoneBookSource.objects.filter(last_name=last_name, props__city=city)
            print(full_name, birth_date)
            print(10*"*" + " addresses " + 10*"*")
            for address in phonebook_set:
                print(
                    address.props["firstname"],
                    address.props["streetname"],
                    address.props["housenumber"],
                    address.props["postalcode"],
                    address.props["city"]
                )
            print(10*"*" + " wieowie " + 10*"*")
            wieowie_set = WieOWieSource.objects.filter(last_name=last_name, props__city=city)
            for info in wieowie_set:
                print(
                    info.props["age"],  # nice opportunity here :)
                    info.props["about_me"]
                )
            print()

    def handle(self, *args, **options):
        self.list_phone_book()
