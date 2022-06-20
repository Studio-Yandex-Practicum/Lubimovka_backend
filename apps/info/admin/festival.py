from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Q

from apps.core.mixins import AdminImagePreview
from apps.core.models import Setting
from apps.info.form import AdditionalLinkForm, ArtTeamMemberForm, FestivalForm, FestTeamMemberForm, PlayLinkForm
from apps.info.models import (
    ArtTeamMember,
    Festival,
    FestivalImage,
    FestivalTeamMember,
    FestTeamMember,
    InfoLink,
    PressRelease,
    Selector,
    Volunteer,
)


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
    form = FestivalForm
    exclude = (
        "teams",
        "sponsors",
        "images",
    )
    empty_value_display = "-пусто-"


@admin.register(PressRelease)
class PressReleaseAdmin(admin.ModelAdmin):
    list_display = ("festival",)
    exclude = ("title",)

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
    form = ArtTeamMemberForm
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
                    "team",
                ),
            },
        ),
    )
    autocomplete_fields = ("person",)
    search_fields = ("position", "person__first_name", "person__last_name")

    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset().filter(team="art")
        return qs


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
                    "team",
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
            if obj.is_pr_director:
                name_director = form.cleaned_data["pr_director_name"]
                FestivalTeamMember.objects.filter(is_pr_director=True).update(is_pr_director=False)
                Setting.objects.filter(settings_key="pr_director_name").update(text=name_director)
            obj = form.save()
        else:
            raise ValidationError("Заполните поля корректно")

    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset().filter(team="fest")
        return qs

    class Media:
        """Adds a script that displays the field ```pr_director_name``` if ```is_pr_director``` is selected."""

        js = ("admin/info/js/FestivalTeamFooter.js",)
