from django.contrib import admin

from apps.core.models import Person
from apps.info.models import (
    Festival,
    FestivalTeam,
    Partner,
    Place,
    Sponsor,
    Volunteer,
)


class PartnerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "type",
        "url",
        "image",
    )
    empty_value_display = "-пусто-"


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "city",
        "image",
    )
    empty_value_display = "-пусто-"


class FestivalTeamAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "person",
        "team",
    )
    empty_value_display = "-пусто-"


class SponsorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "person",
    )
    empty_value_display = "-пусто-"


class VolunteerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "person",
        "year",
    )
    empty_value_display = "-пусто-"


class FestivalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "year",
    )
    empty_value_display = "-пусто-"


class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "city",
        "address",
    )

    list_filter = ("city",)
    search_fields = ("name", "address")


admin.site.register(Partner, PartnerAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(FestivalTeam, FestivalTeamAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Festival, FestivalAdmin)
admin.site.register(Place, PlaceAdmin)
