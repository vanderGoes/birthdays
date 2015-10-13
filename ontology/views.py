from __future__ import unicode_literals

from django.shortcuts import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from ontology.models import FirstName, LastName, Date, Year


def render_ambiguous(request, query_set):
    pass


def first_name_view(request, slug):
    try:
        name = FirstName.objects.get(slug=slug)
    except FirstName.DoesNotExist:
        raise Http404("First name not found.")
    except FirstName.MultipleObjectsReturned:
        # TODO: return disambiguation
        names = FirstName.objects.filter(slug=slug)
        raise HttpResponse("Ambiguous first name {}".format(
            ", ".join(names))
        )
    admin_url = reverse("admin:ontology_firstname_change", args=(name.id,))
    return HttpResponseRedirect(admin_url)


def last_name_view(request, slug):
    try:
        name = LastName.objects.get(slug=slug)
    except LastName.DoesNotExist:
        raise Http404("First name not found.")
    except LastName.MultipleObjectsReturned:
        # TODO: return disambiguation
        names = LastName.objects.filter(slug=slug)
        raise HttpResponse("Ambiguous last name {}".format(
            ", ".join(names))
        )
    admin_url = reverse("admin:ontology_lastname_change", args=(name.id,))
    return HttpResponseRedirect(admin_url)


def date_view(request, slug):
    try:
        date = Date.objects.get(slug=slug)
    except Date.DoesNotExist:
        raise Http404("First name not found.")
    except Date.MultipleObjectsReturned:
        # TODO: return disambiguation
        dates = Date.objects.filter(slug=slug)
        raise HttpResponse("Ambiguous dates {}".format(
            ", ".join(dates))
        )
    admin_url = reverse("admin:ontology_date_change", args=(date.id,))
    return HttpResponseRedirect(admin_url)


def year_view(request, slug):
    try:
        year = Year.objects.get(slug=slug)
    except Year.DoesNotExist:
        raise Http404("First name not found.")
    except Year.MultipleObjectsReturned:
        # TODO: return disambiguation
        years = Year.objects.filter(slug=slug)
        raise HttpResponse("Ambiguous last name {}".format(
            ", ".join(years))
        )
    admin_url = reverse("admin:ontology_lastname_change", args=(year.id,))
    return HttpResponseRedirect(admin_url)
