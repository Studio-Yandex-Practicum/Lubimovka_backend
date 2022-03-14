from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from apps.core.mixins import AdminImagePreview
from apps.core.models import Person, Setting
from apps.info.form import FestivalTeamMemberForm
from apps.info.models import Festival, FestivalTeamMember, Partner, Place, PressRelease, Sponsor, Volunteer


@admin.register(Partner)
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


@admin.register(Person)
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


@admin.register(Volunteer)
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
    classes = ["collapse"]
    ordering = ("person__last_name", "person__first_name")
    classes = ["collapse"]

    @admin.display(
        boolean=True,
        ordering="review_title",
        description="Есть отзыв?",
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
    classes = ["collapse"]


@admin.register(Festival)
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


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "address",
    )

    list_filter = ("city",)
    search_fields = ("name", "address")


@admin.register(PressRelease)
class PressReleaseAdmin(admin.ModelAdmin):
    list_display = ("festival",)
    list_filter = ("festival",)


class PressRealeaseAdmin(admin.ModelAdmin):
    list_display = ("title",)
    list_filter = ("title",)
    search_fields = ("title",)


@admin.register(FestivalTeamMember)
class FestivalTeamMemberAdmin(admin.ModelAdmin):
    form = FestivalTeamMemberForm
    list_display = (
        "person",
        "team",
        "position",
        "is_pr_manager",
    )
    list_filter = (
        "team",
        "is_pr_manager",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "person",
                    "team",
                    "position",
                ),
            },
        ),
        (
            None,
            {
                "fields": (
                    "is_pr_manager",
                    "data_manager",
                ),
                "classes": ("depended_on_team_type",),
            },
        ),
    )

    ordering = ("person__last_name", "person__first_name")

    search_fields = ("position", "person__first_name", "person__last_name")

    def save_model(self, request, obj, form, change):
        """Данные из поля 'data_manager' проверяются и сохраняются в модели 'Setting'."""
        if form.is_valid():
            if obj.is_pr_manager:
                name_manager = form.cleaned_data["data_manager"]
                FestivalTeamMember.objects.filter(is_pr_manager=True).update(is_pr_manager=False)
                Setting.objects.filter(settings_key="pr_manager_name").update(text=name_manager)
            obj.save()
        else:
            raise ValidationError("Заполните поля корректно")

    class Media:
        """Adds a script that displays the field ```is_pr_manager``` if the team art is selected."""

        js = ("admin/info/js/FestivalTeamFooter.js",)


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "position",
    )
