from __future__ import unicode_literals, absolute_import, print_function, division
import six

from rdflib import Graph, URIRef, Literal

from django.apps import apps as django_apps
from django.core.management.base import BaseCommand

from birthdays.models import PersonSource
from ontology.models import LastName, FirstName, Date, Year


class Command(BaseCommand):
    """
    Command output sources to different formats
    """

    @staticmethod
    def graph_from_source(source_model):
        graph = Graph()
        for person in source_model.objects.all():
            person_uri = URIRef(person.get_uri())
            if person.last_name:
                last_name_uri = URIRef(LastName.create_uri(person.last_name))
                graph.add((person_uri, "lastName", last_name_uri))
            if person.first_name:
                first_name_uri = URIRef(FirstName.create_uri(person.first_name))
                graph.add((person_uri, "firstName", first_name_uri))
            if person.birth_date:
                birth_date_uri = URIRef(Date.create_uri(person.birth_date))
                graph.add((person_uri, "birthDate", birth_date_uri))
                year_uri = URIRef(Date.create_uri(person.birth_date.year()))
                graph.add((person_uri, "birthYear", year_uri))
            for key, value in six.iteritems(source_model.props):
                graph.add((person_uri, key, Literal(value)))

        return graph

    @staticmethod
    def output_to_turtle(source_model):
        graph = Command.graph_from_source(source_model)

    def add_arguments(self, parser):
        parser.add_argument(
            'output_type',
            type=unicode,
            help="The output method. Currently only 'output_to_turtle'"
        )
        parser.add_argument(
            '-s', '--source',
            type=unicode,
            help="The source to output."
        )

    def handle(self, *args, **options):
        source_model = django_apps.get_model(app_label="birthdays", model_name=options["source"])
        assert issubclass(source_model, PersonSource), "Specified source {} is not a subclass of PersonSource".format(options["source"])
        handler = getattr(self, options["extend_type"])
        handler(source_model)

