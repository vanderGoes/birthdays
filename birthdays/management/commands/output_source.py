from __future__ import unicode_literals, absolute_import, print_function, division
import six

from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import FOAF, RDF

from django.apps import apps as django_apps
from django.core.management.base import BaseCommand
from django.core.paginator import Paginator

from birthdays.models import PersonSource
from ontology.models import LastName, FirstName, Date, Year


class Command(BaseCommand):
    """
    Command output sources to different formats
    """

    page_size = 100000

    @staticmethod
    def graph_from_page(page):
        graph = Graph()
        for person in page.object_list:
            person_uri = URIRef(person.get_uri())
            graph.add((person_uri, RDF.type, FOAF.Person))
            if person.last_name:
                last_name_uri = URIRef(LastName.create_uri(person.last_name))
                graph.add((person_uri, FOAF.lastName, last_name_uri))
            if person.first_name:
                for name in person.first_name.split(" "):
                    first_name_uri = URIRef(FirstName.create_uri(name))
                    graph.add((person_uri, FOAF.firstName, first_name_uri))
            if person.birth_date:
                birth_date_uri = URIRef(Date.create_uri(person.birth_date))
                graph.add((person_uri, FOAF.birthday, birth_date_uri))
            for key, value in six.iteritems(person.props):
                graph.add((person_uri, BNode(key), Literal(value)))
        return graph

    @staticmethod
    def output_to_turtle(source_model):
        pages = Paginator(source_model.objects.all(), Command.page_size)
        for page_number in pages.page_range:
            graph = Command.graph_from_page(
                pages.page(page_number)
            )
            serialized_graph = graph.serialize(format="turtle", encoding='utf8')
            file_name = "{}-page-{}.ttl".format(
                source_model._meta.model_name,
                page_number
            )
            with open(file_name, "w") as fp:
                fp.write(serialized_graph)

    @staticmethod
    def find_congress_participants(source_model):
        import pandas
        from birthdays.models import Person
        df = pandas.read_csv("../data/congres-deelnemers.csv", encoding="UTF-8")
        for row in df.to_dict(orient="records"):
            first_name = row["Voornaam:"]
            last_name = row["Achternaam:"]
            if "," in last_name:
                name, prefix = last_name.split(",")
                last_name = "{} {}".format(prefix.strip(), name.strip())
            full_name = "{} {}".format(first_name.strip(), last_name.strip())
            for person in Person.objects.filter(full_name=full_name):
                print(full_name)
                print(person.birth_date.strftime("%d-%m-%Y"))
                print(", ".join(set([source._meta.model_name for source in person.sources.all()])))
                print(person.props)
                print()

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
        handler = getattr(self, options["output_type"])
        handler(source_model)

