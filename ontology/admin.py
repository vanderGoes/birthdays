from django.contrib import admin

from ontology.models import LastName, FirstName, Date, Year


class NameOntologyAdmin(admin.ModelAdmin):
    list_display = ["name", "sources"]


class DateOntologyAdmin(admin.ModelAdmin):
    list_display = ["date", "sources"]


class YearOntologyAdmin(admin.ModelAdmin):
    list_display = ["year", "sources"]


admin.site.register(LastName, NameOntologyAdmin)
admin.site.register(FirstName, NameOntologyAdmin)
admin.site.register(Date, DateOntologyAdmin)
admin.site.register(Year, YearOntologyAdmin)
