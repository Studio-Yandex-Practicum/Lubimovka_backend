from django.contrib import admin
from django.utils.html import format_html

from apps.core.mixins import AdminImagePreview
from apps.core.models import Person
from apps.info.models import Festival, FestivalTeam, Partner, Place, PressRelease, Sponsor, Volunteer


class PartnerAdmin(AdminImagePreview, admin.ModelAdmin):
    """Class for registration Partner model in admin panel and expanded with JS script.

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
                ),
            },
        ),
        (
            None,
            {
                "fields": ("in_footer_partner",),
                "classes": ("depended_on_partner_type",),
            },
        ),
        (
            None,
            {
                "fields": (
                    "url",
                    "image",
                    "image_preview_change_page",
                ),
            },
        ),
    )
    empty_value_display = "-пусто-"
    readonly_fields = ("image_preview_change_page",)

    @admin.display(description="Ссылка на сайт")
    def get_partner_url(self, obj):
        """Make the link to the partner's website clickable."""
        return format_html("<a href='{url}'>{url}</a>", url=obj.url)

    class Media:
        """Adds a script that displays the field ```in_footer_partner``` if the general partner is selected."""

        js = ("admin/info/js/PartnerInFooter.js",)


class PersonAdmin(AdminImagePreview, admin.ModelAdmin):
    list_display = (
        "full_name",
        "first_name",
        "last_name",
        "city",
        "image",
        "image_preview_list_page",
    )
    empty_value_display = "-пусто-"
    readonly_fields = ("image_preview_change_page",)


class VolunteerAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "get_year",
        "is_review",
    )
    readonly_fields = ("is_review",)

    @admin.display(
        boolean=True,
        ordering="review_title",
        description="Есть отзыв?",
    )
    def is_review(self, obj):
        """Возвращает: есть ли отзыв."""
        if obj.review_text:
            return True
        return False

    @admin.display(
        ordering="festival",
        description="Год фестиваля",
    )
    def get_year(self, obj):
        """Возвращает год фестиваля."""
        return obj.festival.year


class VolunteerInline(admin.TabularInline):
    model = Volunteer
    readonly_fields = ("is_review",)
    verbose_name = "Волонтёр"
    verbose_name_plural = "Волонтёры"
    extra = 1
    exclude = (
        "review_title",
        "review_text",
    )
    ordering = ("person__first_name",)

    @admin.display(
        boolean=True,
        ordering="review_title",
        description="ОТЗЫВ?",
    )
    def is_review(self, obj):
        if obj.review_text:
            return True
        return False


class FestivalImagesInline(admin.TabularInline):
    model = Festival.images.through
    verbose_name = "Изображение"
    verbose_name_plural = "Изображения"
    extra = 1


class FestivalAdmin(admin.ModelAdmin):
    list_display = ("year",)
    inlines = (
        VolunteerInline,
        FestivalImagesInline,
    )
    exclude = (
        "teams",
        "sponsors",
        "images",
    )
    empty_value_display = "-пусто-"


class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "address",
    )

    list_filter = ("city",)
    search_fields = ("name", "address")


class PressReleaseAdmin(admin.ModelAdmin):
    list_display = ("festival",)
    list_filter = ("festival",)


class PressRealeaseAdmin(admin.ModelAdmin):
    list_display = ("title",)
    list_filter = ("title",)
    search_fields = ("title",)


class FestivalTeamAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "team",
        "position",
    )
    ordering = ("person__first_name",)
    list_filter = ("team",)
    search_fields = ("position", "person__first_name", "person__last_name")


class SponsorAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "position",
    )


admin.site.register(Festival, FestivalAdmin)
admin.site.register(PressRelease, PressReleaseAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(FestivalTeam, FestivalTeamAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Sponsor, SponsorAdmin)
