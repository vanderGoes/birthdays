from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib import admin

from birthdays import views as birthdays_views
from ontology import views as ontology_views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^stats/?$', birthdays_views.stats, name="stats"),
    url(r'^first-names/(?P<slug>[a-z\-]+)/?', ontology_views.first_name_view, name="firstname_view"),
    url(r'^last-names/(?P<slug>[a-z\-]+)/?', ontology_views.last_name_view, name="lastname_view"),
    url(r'^birth-dates/(?P<slug>[0-9\-]+)/?', ontology_views.date_view, name="date_view"),
    url(r'^years/(?P<slug>[0-9\-]+)/?', ontology_views.year_view, name="year_view"),
]
