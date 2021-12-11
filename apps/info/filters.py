from django_filters import FilterSet, filters


class YearPressReleaseFilterSet(FilterSet):
    year = filters.NumberFilter(field_name="festival__year")

    class Meta:
        fields = ("year",)
