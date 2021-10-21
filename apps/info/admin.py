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
    ordering = ("type",)


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "city",
        "image",
    )
    empty_value_display = "-пусто-"


class FestivalTeamInline(admin.TabularInline):
    model = Festival.teams.through
    verbose_name = "Команда и Арт-дирекция"
    verbose_name_plural = "Команда и Арт-дирекция"
    extra = 1


class SponsorInline(admin.TabularInline):
    model = Festival.sponsors.through
    verbose_name = "Попечитель"
    verbose_name_plural = "Попечители"
    extra = 1


class VolunteerInline(admin.TabularInline):
    model = Festival.volunteers.through
    verbose_name = "Волонтёр"
    verbose_name_plural = "Волонтёры"
    extra = 1


class FestivalImagesInline(admin.TabularInline):
    model = Festival.images.through
    verbose_name = "Изображение"
    verbose_name_plural = "Изображения"
    extra = 1


class FestivalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "year",
    )
    inlines = (
        FestivalTeamInline,
        SponsorInline,
        VolunteerInline,
        FestivalImagesInline,
    )
    exclude = (
        "teams",
        "sponsors",
        "volunteers",
        "images",
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


admin.site.register(Festival, FestivalAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(FestivalTeam)
admin.site.register(Volunteer)
admin.site.register(Sponsor)
