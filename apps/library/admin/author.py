from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import re_path

from apps.core import utils
from apps.core.models import Person
from apps.library.models import Author, OtherLink, OtherPlay, SocialNetworkLink


class AchievementInline(admin.TabularInline):
    model = Author.achievements.through
    extra = 1
    verbose_name = "Достижение"
    verbose_name_plural = "Достижения"
    classes = ["collapse"]


class PlayInline(admin.TabularInline):
    model = Author.plays.through
    extra = 1
    verbose_name = "Пьеса"
    verbose_name_plural = "Пьесы"
    classes = ["collapse"]


class SocialNetworkLinkInline(admin.TabularInline):
    model = SocialNetworkLink
    extra = 1
    classes = ["collapse"]


class OtherLinkInline(admin.TabularInline):
    model = OtherLink
    extra = 1
    classes = ["collapse"]


class OtherPlayInline(admin.StackedInline):
    model = OtherPlay
    extra = 1


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
        SocialNetworkLinkInline,
        OtherLinkInline,
        OtherPlayInline,
    )
    exclude = (
        "achievements",
        "plays",
        "social_network_links",
        "other_links",
        "other_plays_links",
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

    class Media:
        js = ("admin/author_slug.js",)
