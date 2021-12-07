from django_filters import rest_framework as filters

from apps.library.models import Play


class PlayFilter(filters.FilterSet):
    program = filters.BaseInFilter(
        field_name="program__pk",
        label="Программа",
    )
    festival = filters.BaseInFilter(
        field_name="festival__year",
        label="Год фестиваля",
    )

    class Meta:
        model = Play
        fields = (
            "program",
            "festival",
        )
