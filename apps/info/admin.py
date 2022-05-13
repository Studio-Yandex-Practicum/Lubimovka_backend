from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.html import format_html

from apps.core.mixins import AdminImagePreview
from apps.core.models import Person, Setting
from apps.info.filters import FestivalYearFilter, HasReviewAdminFilter, PartnerTypeFilter
from apps.info.form import AdditionalLinkForm, FestTeamMemberForm, PlayLinkForm
from apps.info.models import (
    Festival,
    FestivalImage,
    FestivalTeamMember,
    InfoLink,
    Partner,
    Place,
    PressRelease,
    Selector,
    Sponsor,
    Volunteer,
)
from apps.info.models.festival import ArtTeamMember, FestTeamMember


@admin.register(Partner)
class PartnerAdmin(SortableAdminMixin, AdminImagePreview, admin.ModelAdmin):
    """Class for registration Partner model in admin panel and expanded with JS script.

    There are used two classes in fieldsets: `predefined` and `included`.
    These classes are not in the documentation and this names are invented
    by developer for the script to work.

    `predefined` - if partners are festival or info.
    `included` - if partner is general.
    """

    list_display = (
        "order",
        "name",
        "type",
        "get_partner_url",
        "image_preview_list_page",
    )
    list_display_links = ("name",)
    list_filter = (PartnerTypeFilter,)
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
    list_display_links = ("person",)
    autocomplete_fields = ("person",)
    readonly_fields = ("is_review",)
    list_filter = (
        FestivalYearFilter,
        HasReviewAdminFilter,
    )

    @admin.display(
        ordering="festival",
        description="Год фестиваля",
    )
    def get_year(self, obj):
        """Возвращает год фестиваля."""
        return obj.festival.year

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


class VolunteerInline(SortableInlineAdminMixin, admin.TabularInline):
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
    classes = ("collapsible",)

    @admin.display(
        boolean=True,
        ordering="review_title",
        description="Есть отзыв?",
    )
    def is_review(self, obj):
        if obj.review_text:
            return True
        return False


class SelectorInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Selector
    autocomplete_fields = ("person",)
    verbose_name = "Отборщик"
    verbose_name_plural = "Отборщики"
    extra = 1
    classes = ("collapsible",)


class FestivalImagesInline(admin.TabularInline, AdminImagePreview):
    model = FestivalImage
    readonly_fields = ("image_preview_list_page",)
    verbose_name = "Изображение"
    verbose_name_plural = "Изображения"
    extra = 1
    classes = ("collapsible",)
    model.__str__ = lambda self: ""


class PlayInfoLinkInline(SortableInlineAdminMixin, admin.TabularInline):
    model = InfoLink
    form = PlayLinkForm
    extra = 0
    verbose_name = "Пьесы (ссылки)"
    verbose_name_plural = "Пьесы (ссылки)"
    classes = ("collapsible",)

    def get_queryset(self, request):
        return InfoLink.objects.filter(type=InfoLink.LinkType.PLAYS_LINKS)


class AdditionalInfoLinkInline(SortableInlineAdminMixin, admin.TabularInline):
    model = InfoLink
    form = AdditionalLinkForm
    extra = 0
    verbose_name = "Дополнительно (ссылки)"
    verbose_name_plural = "Дополнительно (ссылки)"
    classes = ("collapsible",)

    def get_queryset(self, request):
        return InfoLink.objects.filter(type=InfoLink.LinkType.ADDITIONAL_LINKS)


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    inlines = (
        VolunteerInline,
        SelectorInline,
        FestivalImagesInline,
        PlayInfoLinkInline,
        AdditionalInfoLinkInline,
    )
    exclude = (
        "teams",
        "sponsors",
        "images",
    )
    empty_value_display = "-пусто-"


@admin.register(Place)
class PlaceAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = (
        "order",
        "name",
        "city",
        "address",
    )
    list_display_links = ("name",)
    list_filter = ("city",)
    search_fields = ("name", "address")


@admin.register(PressRelease)
class PressReleaseAdmin(admin.ModelAdmin):
    list_display = ("festival",)

    def get_form(self, request, obj=None, **kwargs):
        """Set free festivals and current festivals if exists."""
        form = super().get_form(request, obj, **kwargs)
        current_id = None if not obj else obj.festival_id
        form.base_fields["festival"].queryset = Festival.objects.filter(
            Q(press_releases__festival__isnull=True) | Q(id=current_id)
        )
        return form


@admin.register(ArtTeamMember)
class ArtTeamMemberAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = (
        "order",
        "person",
        "position",
    )
    list_display_links = ("person",)
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
class FestTeamMemberAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = FestTeamMemberForm
    list_display = (
        "order",
        "person",
        "position",
        "is_pr_director",
    )
    list_display_links = ("person",)
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
                "fields": ("pr_director_name",),
                "classes": ("form-row field-pr_director_name",),
            },
        ),
    )
    autocomplete_fields = ("person",)
    search_fields = ("position", "person__first_name", "person__last_name")

    def save_model(self, request, obj, form, change):
        """Данные из поля 'pr_director_name' проверяются и сохраняются в модели 'Setting'."""
        if form.is_valid():
            team = "fest"
            if obj.is_pr_director:
                name_director = form.cleaned_data["pr_director_name"]
                FestivalTeamMember.objects.filter(is_pr_director=True).update(is_pr_director=False)
                Setting.objects.filter(settings_key="pr_director_name").update(text=name_director)
            obj = form.save(commit=False)
            obj.team = team
            obj.save()
        else:
            raise ValidationError("Заполните поля корректно")

    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset().filter(team="fest")
        return qs

    class Media:
        """Adds a script that displays the field ```pr_director_name``` if ```is_pr_director``` is selected."""

        js = ("admin/info/js/FestivalTeamFooter.js",)


@admin.register(Sponsor)
class SponsorAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = (
        "order",
        "person",
        "position",
    )
    list_display_links = ("person",)
    autocomplete_fields = ("person",)


@admin.register(Selector)
class SelectorAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "get_year",
        "position",
    )
    list_display_links = ("person",)
    autocomplete_fields = ("person",)
    list_filter = (FestivalYearFilter,)

    @admin.display(
        ordering="festival",
        description="Год фестиваля",
    )
    def get_year(self, obj):
        """Возвращает год фестиваля."""
        return obj.festival.year
