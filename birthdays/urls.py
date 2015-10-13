from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib import admin

from birthdays import views as birthdays_views
from ontology import views as ontology_views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^stats/?$', birthdays_views.stats, name="stats"),
    url(r'^first-names/(?P<slug>[a-z\-]+)/?', ontology_views.first_names, name="first_names"),
    url(r'^last-names/(?P<slug>[a-z\-]+)/?', ontology_views.last_names, name="last_names"),
]
