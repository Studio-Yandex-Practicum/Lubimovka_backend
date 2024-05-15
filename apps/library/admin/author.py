from functools import partial
from typing import Any, Optional, Union

from adminsortable2.admin import SortableInlineAdminMixin
from django import forms
from django.contrib import admin, messages
from django.contrib.postgres.aggregates import StringAgg
from django.db.models import Count
from django.forms import ModelForm, ValidationError
from django.forms.fields import Field
from django.http.request import HttpRequest

from apps.core.mixins import PreviewButtonMixin
from apps.core.services.mail_forwarding import on_change
from apps.library.forms import OtherLinkForm
from apps.library.models import Author, AuthorPlay, OtherLink, SocialNetworkLink
from apps.postfix.models import Virtual


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
        "play_programs",
    )

    def get_queryset(self, request):
        return (
            AuthorPlay.objects.filter(play__other_play=False)
            .select_related(
                "author__person",
                "play__festival",
            )
            .annotate(program_list=StringAgg("play__programs__name", ", "))
        )

    @admin.display(description="Год участия в фестивале")
    def play_festival_year(self, obj):
        return f"{obj.play.festival.year}"

    @admin.display(description="Программы")
    def play_programs(self, obj):
        return f"{obj.program_list}"


class OtherPlayInline(SortableInlineAdminMixin, admin.TabularInline):
    form = PlayInlineForm
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


class AchievementInline(admin.TabularInline):
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
        return f"{obj.program_list} - {obj.play.festival.year}"

    def get_queryset(self, request):
        return (
            AuthorPlay.objects.filter(play__other_play=False)
            .select_related("author__person", "play__festival")
            .order_by("-play__festival__year")
            .annotate(program_list=StringAgg("play__programs__name", ", "))
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


class AuthorAdminForm(forms.ModelForm):
    enable_email = forms.BooleanField(required=False, initial=False, label="Включить переадресацию почты")

    def get_initial_for_field(self, field: Field, field_name: str) -> Any:
        if self.instance.pk and field is self.fields["enable_email"]:
            if hasattr(self.instance, "virtual_email"):
                return self.instance.virtual_email.enabled
            return False
        return super().get_initial_for_field(field, field_name)

    def clean(self):
        cleaned_data = super().clean()
        enable_email = cleaned_data.get("enable_email")
        person = cleaned_data.get("person")
        slug = cleaned_data.get("slug")
        if enable_email and Virtual.objects.filter(mailbox=slug).exists():
            raise ValidationError(
                "Такой почтовый ящик уже существует. Измените транслит фамилии или отключите переадресацию."
            )
        if enable_email and person:
            if not person.email:
                raise ValidationError(
                    "Нельзя включить перенаправление электронной почты так как у персоны не указан адрес"
                )


@admin.register(Author)
class AuthorAdmin(PreviewButtonMixin, admin.ModelAdmin):
    # form = AuthorAdminForm
    list_display = (
        "person",
        "quote",
        "slug",
        "plays_count",
        "forwarding",
    )
    inlines = (
        PlayInline,
        OtherPlayInline,
        SocialNetworkLinkInline,
        OtherLinkInline,
        AchievementInline,
    )
    exclude = (
        "plays",
        "social_network_links",
        "other_links",
    )
    search_fields = (
        "biography",
        "slug",
        "person__first_name__unaccent",
        "person__last_name__unaccent",
        "person__middle_name__unaccent",
        "person__email",
        "plays__name",
    )
    autocomplete_fields = ("person",)
    empty_value_display = "-пусто-"

    def get_readonly_fields(self, request: HttpRequest, obj: Optional[Any] = ...) -> Union[list[str], tuple[Any, ...]]:
        fields = super().get_readonly_fields(request, obj)
        if hasattr(obj, "virtual_email") and not request.user.has_perm("postfix.change_virtual"):
            fields = list(fields) + ["person", "slug"]
        return fields

    def get_form(self, request, obj=None, change=False, **kwargs) -> Any:
        if request.user.has_perm("postfix.add_virtual") and request.user.has_perm("postfix.change_virtual"):
            kwargs["form"] = AuthorAdminForm
        return super().get_form(request, obj, change, **kwargs)

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related("person").select_related("virtual_email")
        queryset = queryset.annotate(
            _plays_count=Count("plays", distinct=True),
        )
        return queryset

    def save_related(self, request: Any, form: Any, formsets: Any, change: Any) -> None:
        author: Author = form.instance
        has_changes = any(field_name in form.changed_data for field_name in ["enable_email", "person", "slug"])
        if has_changes:
            on_change(
                author,
                create=form.cleaned_data.get("enable_email", False),
                message=partial(messages.add_message, request, messages.INFO),
            )
        return super().save_related(request, form, formsets, change)

    @admin.display(description="Количество пьес")
    def plays_count(self, obj):
        return obj._plays_count

    @admin.display(description="Почта", boolean=True)
    def forwarding(self, obj):
        return hasattr(obj, "virtual_email") and obj.virtual_email.enabled

    class Media:
        js = ("admin/author_admin.js",)
