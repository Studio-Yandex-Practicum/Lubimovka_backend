from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django import forms
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.html import format_html

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
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "review_text":
            kwargs["widget"] = forms.Textarea(
                attrs={
                    "style": "width:400px; height:60px;",
                    "readonly": "readonly",
                }
            )
        return super(VolunteerInline, self).formfield_for_dbfield(db_field, **kwargs)

    model = Volunteer
    autocomplete_fields = ("person",)
    readonly_fields = (
        "is_review",
        "change_review",
    )
    verbose_name = "Волонтёр"
    verbose_name_plural = "Волонтёры"
    extra = 1
    exclude = ("review_title",)
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

    @admin.display(
        description="",
    )
    def change_review(self, obj):
        if obj.pk:
            opts = self.model._meta
            redirect_url = reverse(
                "admin:%s_%s_change" % (opts.app_label, "review"),
                args=(obj.pk,),
                current_app=self.admin_site.name,
            )
            return format_html(f"<a href='{redirect_url}'>Изменить отзыв</a>")
        return None


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

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if obj:
            return fields + ("festival",)
        return fields


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

    def has_delete_permission(self, request, obj=None):
        if obj and obj.is_pr_director:
            messages.add_message(
                request,
                messages.ERROR,
                ("Для того чтобы снять с должности PR-директора, " "нужно назначить другого человека на эту должность"),
            )
            return False
        return super().has_delete_permission(request, obj)

    class Media:
        """Adds a script that displays the field ```pr_director_name``` if ```is_pr_director``` is selected."""

        css = {"all": ("admin/info/css/pr.css",)}
        js = ("admin/info/js/FestivalTeamFooter.js",)
