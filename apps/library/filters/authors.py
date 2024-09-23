import django_filters
from django.db.models import Q


def filter_by_name_predicate(queryset, name, value):
    """Фамилии начинающиеся не с кирилицы выдается под знаком '#'."""
    if value == "#":
        return queryset.exclude(Q(person__last_name__regex="^[а-яА-Я]"))
    return queryset.filter(Q(person__last_name__unaccent__istartswith=value))


class AuthorFilter(django_filters.FilterSet):
    """Фильтрует по начальным буквам в фамилии и имени."""

    letter = django_filters.CharFilter(method=filter_by_name_predicate)
