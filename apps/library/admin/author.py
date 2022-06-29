from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.forms import ModelForm, ValidationError

from apps.library.forms import OtherLinkForm
from apps.library.models import Author, AuthorPlay, OtherLink, SocialNetworkLink


class PlayInlineForm(ModelForm):
    """Форма, проверяющая возможность удаления пьесы из списка автора."""

    def clean_DELETE(self):
        data = self.cleaned_data["DELETE"]
        if data and self.instance.play.author_plays.count() == 1:
            error = ValidationError("Эта пьеса не может быть удалена, так как это единственный её автор")
            self.add_error(field=None, error=error)
            raise error
        return data


class PlayInline(SortableInlineAdminMixin, admin.TabularInline):
    form = PlayInlineForm
    model = AuthorPlay
    extra = 0
    verbose_name = "Пьеса"
    verbose_name_plural = "Пьесы"
    classes = ("collapsible",)
    autocomplete_fields = ("play",)
    readonly_fields = (
        "play_festival_year",
        "play_program",
    )

    def get_queryset(self, request):
        return AuthorPlay.objects.filter(play__other_play=False).select_related(
            "author__person",
            "play",
        )

    @admin.display(description="Год участия в фестивале")
    def play_festival_year(self, obj):
        return f"{obj.play.festival.year}"

    @admin.display(description="Программа")
    def play_program(self, obj):
        return f"{obj.play.program}"


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
        "slug",
        "number_of_plays",
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

    class Media:
        js = ("admin/author_admin.js",)
