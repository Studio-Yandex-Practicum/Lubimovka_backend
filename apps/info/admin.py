from django.contrib import admin

from apps.core.mixins import AdminImagePreview
from apps.core.models import Person
from apps.info.models import (
    Festival,
    FestivalTeam,
    Partner,
    Place,
    Sponsor,
    Volunteer,
)


class PartnerAdmin(AdminImagePreview, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "type",
        "url",
        "image",
        "image_preview_list_page",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "type",
                    "url",
                    "image",
                    "image_preview_change_page",
                ),
                "classes": ("predefined",),
            },
        ),
        (
            None,
            {
                "fields": ("in_footer",),
                "classes": ("included",),
            },
        ),
    )
    empty_value_display = "-пусто-"
    ordering = ("type",)
    readonly_fields = ("image_preview_change_page",)

    class Media:
        js = ("admin/js/partnerisfooter.js",)


class PersonAdmin(AdminImagePreview, admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "city",
        "image",
        "image_preview_list_page",
    )
    empty_value_display = "-пусто-"
    readonly_fields = ("image_preview_change_page",)


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
