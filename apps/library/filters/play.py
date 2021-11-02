from django_filters import rest_framework as filters

from apps.library.models import Play


class PlayFilter(filters.FilterSet):
    program = filters.AllValuesMultipleFilter(
        field_name="program__name",
    )
    festival = filters.AllValuesMultipleFilter(
        field_name="festival__year",
    )

    class Meta:
        model = Play
        fields = ["program", "festival"]
