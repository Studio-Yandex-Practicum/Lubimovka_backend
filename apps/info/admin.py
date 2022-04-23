from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from apps.core.mixins import AdminImagePreview
from apps.core.models import Person, Setting
from apps.info.filters import HasReviewAdminFilter
from apps.info.form import FestTeamMemberForm
from apps.info.models import (
    Festival,
    FestivalTeamMember,
    Partner,
    Place,
    PressRelease,
    Question,
    Selector,
    Sponsor,
    Volunteer,
)
from apps.info.models.festival import ArtTeamMember, FestTeamMember


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
    search_fields = ("name",)
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
    search_fields = (
        "first_name",
        "last_name",
    )
    list_filter = ("city",)
    empty_value_display = "-пусто-"
    readonly_fields = ("image_preview_change_page",)


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "get_year",
        "is_review",
    )
    autocomplete_fields = ("person",)
    readonly_fields = ("is_review",)
    list_filter = (
        "festival",
        HasReviewAdminFilter,
    )

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
    autocomplete_fields = ("person",)
    readonly_fields = ("is_review",)
    verbose_name = "Волонтёр"
    verbose_name_plural = "Волонтёры"
    extra = 1
    exclude = (
        "review_title",
        "review_text",
    )
    classes = ["collapsible"]
    ordering = ("person__last_name", "person__first_name")

    @admin.display(
        boolean=True,
        ordering="review_title",
        description="Есть отзыв?",
    )
    def is_review(self, obj):
        if obj.review_text:
            return True
        return False


class FestivalImagesInline(admin.TabularInline, AdminImagePreview):
    model = Festival.images.through
    readonly_fields = ("inline_image_preview",)
    verbose_name = "Изображение"
    verbose_name_plural = "Изображения"
    extra = 1
    classes = ["collapsible"]
    model.__str__ = lambda self: ""


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


@admin.register(ArtTeamMember)
class ArtTeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "team",
        "position",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "person",
                    "position",
                ),
            },
        ),
    )

    ordering = ("person__last_name", "person__first_name")
    autocomplete_fields = ("person",)
    search_fields = ("position", "person__first_name", "person__last_name")

    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset().filter(team="art")
        return qs

    def save_model(self, request, obj, form, change):
        """Устанваливается поле "team" на значение "art"."""
        if form.is_valid():
            team = "art"
            obj = form.save(commit=False)
            obj.team = team
            obj.save()
        else:
            raise ValidationError("Заполните поля корректно")


@admin.register(FestTeamMember)
class FestTeamMemberAdmin(admin.ModelAdmin):
    form = FestTeamMemberForm
    list_display = (
        "person",
        "team",
        "position",
        "is_pr_director",
    )
    list_filter = ("is_pr_director",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "person",
                    "position",
                    "is_pr_director",
                ),
            },
        ),
        (
            None,
            {
                "fields": ("pr_directore_dative_name",),
                "classes": ("form-row field-pr_directore_dative_name",),
            },
        ),
    )

    ordering = ("person__last_name", "person__first_name")
    autocomplete_fields = ("person",)
    search_fields = ("position", "person__first_name", "person__last_name")

    def save_model(self, request, obj, form, change):
        """Данные из поля 'pr_directore_dative_name' проверяются и сохраняются в модели 'Setting'."""
        if form.is_valid():
            team = "fest"
            if obj.is_pr_director:
                name_director = form.cleaned_data["pr_directore_dative_name"]
                FestivalTeamMember.objects.filter(is_pr_director=True).update(is_pr_director=False)
                Setting.objects.filter(settings_key="pr_directore_dative_name").update(text=name_director)
            obj = form.save(commit=False)
            obj.team = team
            obj.save()
        else:
            raise ValidationError("Заполните поля корректно")

    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset().filter(team="fest")
        return qs

    class Media:
        """Adds a script that displays the field ```pr_directore_dative_name``` if ```is_pr_director``` is selected."""

        js = ("admin/info/js/FestivalTeamFooter.js",)


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "position",
    )
    autocomplete_fields = ("person",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "author_name", "author_email", "question", "sent")
    list_filter = ("sent",)

    def has_module_permission(self, request):
        if request.user.is_authenticated and (request.user.is_admin or request.user.is_superuser):
            return super().has_module_permission(request)
        return False


@admin.register(Selector)
class SelectorAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "get_year",
        "position",
    )
    autocomplete_fields = ("person",)

    @admin.display(
        ordering="festival",
        description="Год фестиваля",
    )
    def get_year(self, obj):
        """Возвращает год фестиваля."""
        return obj.festival.year
