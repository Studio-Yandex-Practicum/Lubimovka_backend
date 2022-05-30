from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import re_path

from apps.core import utils
from apps.core.models import Person
from apps.library.forms import OtherLinkForm
from apps.library.models import Author, AuthorPlay, OtherLink, Play, SocialNetworkLink


class PlayInline(SortableInlineAdminMixin, admin.TabularInline):
    model = AuthorPlay
    extra = 0
    verbose_name = "Пьеса"
    verbose_name_plural = "Пьесы"
    classes = ("collapsible",)
    autocomplete_fields = ("play",)

    def get_queryset(self, request):
        return AuthorPlay.objects.filter(play__other_play=False).select_related(
            "author__person",
            "play",
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Play.objects.filter(other_play=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = ("admin/play_autocomplete.js",)


class OtherPlayInline(SortableInlineAdminMixin, admin.TabularInline):
    model = AuthorPlay
    extra = 0
    verbose_name = "Другая пьеса"
    verbose_name_plural = "Другие пьесы"
    classes = ("collapsible",)
    autocomplete_fields = ("play",)

    def get_queryset(self, request):
        return AuthorPlay.objects.filter(play__other_play=True).select_related(
            "author__person",
            "play",
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Play.objects.filter(other_play=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = ("admin/otherplay_autocomplete.js",)


class AchivementInline(admin.TabularInline):
    model = AuthorPlay
    extra = 0
    verbose_name = "Достижение"
    verbose_name_plural = "Достижения"
    classes = ("collapsible",)
    fields = ("achievement",)
    readonly_fields = ("achievement",)

    @admin.display(
        description="Достижения",
    )
    def achievement(self, obj):
        return f"{obj.play.program} - {obj.play.festival.year}"

    def get_queryset(self, request):
        return (
            AuthorPlay.objects.filter(play__other_play=False)
            .select_related("author__person", "play__program", "play__festival")
            .order_by("-play__festival__year")
            .distinct("play__festival__year", "play__program")
        )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SocialNetworkLinkInline(admin.TabularInline):
    model = SocialNetworkLink
    extra = 1
    classes = ("collapsible",)


class OtherLinkInline(SortableInlineAdminMixin, admin.TabularInline):
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
        PlayInline,
        OtherPlayInline,
        SocialNetworkLinkInline,
        OtherLinkInline,
        AchivementInline,
    )
    exclude = (
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

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("person")

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
