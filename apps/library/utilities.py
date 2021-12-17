from collections import defaultdict

from django.db.models import Value
from django.db.models.functions import Concat

from apps.info.models import Festival


def generate_class_name_path(instance, filename):
    festival = Festival.objects.last()
    return f"{instance.__class__.__name__}/{festival.year}/{filename}"


def team_collector(model, filters: dict = None) -> defaultdict:
    """
    Group team members by roles.

    Form dictionary with next structure:
    {
        "Драматург": [
            "Мария Ефимова",
            "Ефимов Иван"
        ],
        "Режиссёр": [
            "Арефий Лукин"
        ],
        ...
    }
    Duplication of role, name pairs should be avoided by model's constraints.
    """
    qs = (
        model.objects.filter(**filters)
        .values_list("role__name")
        .annotate(name=Concat("person__first_name", Value(" "), "person__last_name"))
    )
    team = defaultdict(list)
    for key, value in qs:
        team[key].append(value)
    return team


def team_collector_with_plural_slug(model, filters: dict = None) -> defaultdict:
    """
    Group team members by roles.
    Make plural slug for Role.
    Form dictionary with next structure:
    {
        "Dramatists": [
            "Мария Ефимова",
            "Ефимов Иван"
        ],
        "Directors": [
            "Арефий Лукин"
        ],
        ...
    }
    Duplication of role, name pairs should be avoided by model's constraints.
    """

    qs = (
        model.objects.filter(**filters)
        .values_list("role__slug")
        .annotate(name=Concat("person__first_name", Value(" "), "person__last_name"))
    )
    team = defaultdict(list)
    for key, value in qs:
        key += "s"
        team[key].append(value)
    return team
