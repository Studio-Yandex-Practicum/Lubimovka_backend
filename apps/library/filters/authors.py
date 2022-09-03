import django_filters
from django.db.models import Q

from apps.library.utilities import has_cyrillic


def filter_by_name_predicate(queryset, name, value):
    """Имена и фамилии начинающиеся не с кирилицы выдается под знаком '$'."""
    if has_cyrillic(value):
        return queryset.filter(Q(person__first_name__istartswith=value) | Q(person__last_name__istartswith=value))
    if value == "$":
        return queryset.exclude(Q(person__first_name__regex="^[а-яА-Я]") | Q(person__last_name__regex="^[а-яА-Я]"))


class AuthorFilter(django_filters.FilterSet):
    """Фильтрует по начальным буквам в фамилии и имени."""

    letter = django_filters.CharFilter(method=filter_by_name_predicate)
