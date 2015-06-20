
from django.apps import apps
from django.db.models import Count
from django.shortcuts import render_to_response, RequestContext

from .models import Person, PersonSource, GeneratedPerson




def stats(request):
    app = apps.get_app("birthdays")
    sources = [
        model for model in apps.get_models(app)
        if issubclass(model, PersonSource)
    ][2:]  # first two are base classes not actual sources
    stats = [
        ("Master records total", Person.objects.count()),
        ("Extended records total", Person.objects.annotate(num_sources=Count("sources")).filter(num_sources__gt=1).count()),
        ("Number of sources", len(sources) - 3),  # there are 3 test sources
        ("Source records total", PersonSource.objects.count()),
        ("Sourcing records total", PersonSource.objects.filter(master__isnull=False).count()),
    ]
    return render_to_response("stats.html", {"stats": stats}, RequestContext(request))
