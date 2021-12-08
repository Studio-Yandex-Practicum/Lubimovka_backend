from django.contrib import admin
from django.utils.html import format_html

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
    """Class for registration Partner model in admin panel and expanded
    with JS script.

    There are used two classes in fieldsets: `predefined` and `included`.
    These classes are not in the documentation and this names are invented
    by developer for the script to work.

    `predefined` - if partners are festival or info.
    `included` - if partner is general.
    """

    list_display = (
        "name",
        "type",
        "get_partner_url",
        "image_preview_list_page",
    )
    list_filter = ("type",)
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
                "fields": ("in_footer_partner",),
                "classes": ("included",),
            },
        ),
    )
    empty_value_display = "-пусто-"
    readonly_fields = ("image_preview_change_page",)

    @admin.display(description="Ссылка на сайт")
    def get_partner_url(self, obj):
        """Makes the link to the partner's website clickable."""
        return format_html("<a href='{url}'>{url}</a>", url=obj.url)

    class Media:
        """Adds a script that displays the field ```in_footer_partner```
        if the general partner is selected.
        """

        js = ("admin/js/PartnerInFooter.js",)


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
