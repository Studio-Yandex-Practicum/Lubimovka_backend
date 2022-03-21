from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from apps.library.models import Play


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class PlayFilter(filters.FilterSet):
    program = NumberInFilter(
        field_name="program__pk",
        label="Программа",
        lookup_expr="in",
    )
    festival = NumberInFilter(
        field_name="festival__year",
        label="Год фестиваля",
        lookup_expr="in",
    )

    class Meta:
        model = Play
        fields = (
            "program",
            "festival",
        )


class PlayTypeFilter(admin.SimpleListFilter):
    title = _("Тип пьесы")
    parameter_name = "play_type"

    def lookups(self, request, model_admin):
        return (
            (None, _("Пьесы Любимовки")),
            ("other", _("Показать другие пьесы")),
            ("all", _("Показать все")),
        )

    def queryset(self, request, queryset):
        if self.value() == "other":
            return Play.objects.filter(play_type="OTHER")
        if self.value() is None:
            return Play.objects.filter(play_type="MAIN")

    def choices(self, changelist):
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == lookup,
                "query_string": changelist.get_query_string(
                    {
                        self.parameter_name: lookup,
                    },
                    [],
                ),
                "display": title,
            }
