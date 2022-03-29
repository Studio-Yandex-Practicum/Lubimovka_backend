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
    published = filters.BooleanFilter(
        field_name="published",
        label="Отображать только опубликованные пьесы?",
    )

    class Meta:
        model = Play
        fields = (
            "program",
            "festival",
        )
