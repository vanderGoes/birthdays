from django.contrib import admin

from birthdays.models import Person, NBASource, BIGSource, PhoneBookSource, WieOWieSource, WikiSource, SchoolBankSource


class PersonSourceAdmin(admin.ModelAdmin):
    list_display = ["full_name", "birth_date", "props"]


admin.site.register(Person, PersonSourceAdmin)
admin.site.register(NBASource, PersonSourceAdmin)
admin.site.register(BIGSource, PersonSourceAdmin)
admin.site.register(PhoneBookSource, PersonSourceAdmin)
admin.site.register(WieOWieSource, PersonSourceAdmin)
admin.site.register(WikiSource, PersonSourceAdmin)
admin.site.register(SchoolBankSource, PersonSourceAdmin)