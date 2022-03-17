from django.contrib import admin

from apps.core.models import Person
from apps.library.forms.admin import AuthorForm
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


class AuthorAdmin(admin.ModelAdmin):
    form = AuthorForm
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
        if not request.user.has_perm("library.can_change_author"):
            return form
        if obj:
            form.base_fields["person"].queryset = Person.objects.exclude(authors__in=Author.objects.exclude(id=obj.id))
        else:
            form.base_fields["person"].queryset = Person.objects.exclude(authors__in=Author.objects.all())
        return form


admin.site.register(Author, AuthorAdmin)
