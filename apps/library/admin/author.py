from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import re_path

from apps.core import utils
from apps.core.models import Person
from apps.library.forms.admin import OtherLinkForm
from apps.library.models import Achievement, Author, AuthorPlay, OtherLink, Play, SocialNetworkLink
from apps.library.utilities import CustomAutocompleteSelect


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    search_fields = ("tag",)


class AchievementInline(admin.TabularInline):
    model = Author.achievements.through
    extra = 1
    verbose_name = "Достижение"
    verbose_name_plural = "Достижения"
    classes = ("collapsible",)


class PlayInline(SortableInlineAdminMixin, admin.TabularInline):
    model = AuthorPlay
    extra = 0
    verbose_name = "Пьеса"
    verbose_name_plural = "Пьесы"
    classes = ("collapsible",)

    def get_queryset(self, request):
        return AuthorPlay.objects.exclude(play__program__slug="other_plays")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Play.objects.exclude(program__slug="other_plays")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class OtherPlayInline(SortableInlineAdminMixin, admin.TabularInline):
    model = AuthorPlay
    extra = 0
    verbose_name = "Другая пьеса"
    verbose_name_plural = "Другие пьесы"
    classes = ("collapsible",)

    def get_queryset(self, request):
        return AuthorPlay.objects.filter(play__program__slug="other_plays")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Play.objects.filter(program__slug="other_plays")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SocialNetworkLinkInline(admin.TabularInline):
    model = SocialNetworkLink
    extra = 1
    classes = ("collapsible",)


class OtherLinkInline(admin.TabularInline):
    form = OtherLinkForm
    model = OtherLink
    extra = 1
    classes = ("collapsible",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "quote",
        "biography",
        "slug",
    )
    inlines = (
        AchievementInline,
        PlayInline,
        OtherPlayInline,
        SocialNetworkLinkInline,
        OtherLinkInline,
    )
    exclude = (
        "achievements",
        "plays",
        "social_network_links",
        "other_links",
    )
    search_fields = (
        "biography",
        "slug",
        "person__first_name",
        "person__last_name",
        "person__middle_name",
        "person__email",
        "plays__name",
    )
    autocomplete_fields = ("person",)
    empty_value_display = "-пусто-"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm("library.change_author"):
            return form
        if obj:
            form.base_fields["person"].queryset = Person.objects.exclude(authors__in=Author.objects.exclude(id=obj.id))
        else:
            form.base_fields["person"].queryset = Person.objects.exclude(authors__in=Author.objects.all())
        return form

    def get_urls(self):
        urls = super().get_urls()
        ajax_urls = [
            re_path(r"\S*/ajax_author_slug/", self.author_slug),
        ]
        return ajax_urls + urls

    def author_slug(self, request, obj_id=None):
        person_id = request.GET.get("person")
        person = get_object_or_404(Person, id=person_id)
        slug = utils.slugify(person.last_name)
        response = {"slug": slug}
        return JsonResponse(response)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "person":
            db = kwargs.get("using")
            kwargs["widget"] = CustomAutocompleteSelect(
                db_field, self.admin_site, using=db, placeholder="Выберите человека"
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
