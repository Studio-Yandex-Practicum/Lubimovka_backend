import re

from django.db.models.query import Prefetch

from apps.core.models import Role


def get_team_roles(obj, filters: dict = None):
    """Return all roles used in event.

    Collects persons related with role using Prefetch.
    """
    roles = Role.objects.filter(**filters).distinct()
    team = obj.team_members.all()
    return roles.prefetch_related(Prefetch("team_members", team))


def has_cyrillic(text):
    """Проверка на кирилицу."""
    return bool(re.search("[а-яА-Я]", text))


def filter_letter_values(queryset):
    """Возвращает список всех начльных букв в имени и фамилии.

    Если имя или фамилилия не на кирилице, используется символ '#'.
    """
    letters_values_set = set()
    for author in queryset:
        letter = author.get("letter").upper()
        if has_cyrillic(letter):
            letters_values_set.add(letter)
        if not has_cyrillic(letter):
            letter = "#"
            letters_values_set.add(letter)
    return sorted(letters_values_set)
