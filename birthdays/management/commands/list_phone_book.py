from __future__ import unicode_literals, absolute_import, print_function, division

from django.core.management.base import BaseCommand

from birthdays.models import NBASource, PhoneBookSource, WieOWieSource


class Command(BaseCommand):
    """
    Command to list all the people we have more information on than average.
    """

    @staticmethod
    def list_phone_book():
        for accountant in NBASource.objects.all()[:1000]:
            full_name = accountant.full_name
            birth_date = accountant.birth_date
            last_name = accountant.last_name
            city = accountant.props["city"]
            if not city:
                continue
            city = city.lower().capitalize()
            phonebook_set = PhoneBookSource.objects.filter(last_name=last_name, props__city=city)
            print(full_name, birth_date)
            print(10*"*" + " addresses " + 10*"*")
            for address in phonebook_set:
                print(
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
