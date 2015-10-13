from __future__ import unicode_literals

from django.shortcuts import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from ontology.models import FirstName, LastName


def render_ambiguous(request, query_set):
    pass


def first_names(request, slug):
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


def last_names(request, slug):
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
