import django_filters


class AuthorFilter(django_filters.FilterSet):
    letter = django_filters.CharFilter(
        field_name="person__last_name", lookup_expr="startswith"
    )

    class Meta:
        fields = ("letter",)
