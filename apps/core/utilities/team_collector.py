from collections import defaultdict

from django.db.models import Value
from django.db.models.functions import Concat


def team_collector(model, filters: dict = None) -> defaultdict:
    qs = (
        model.objects.filter(**filters)
        .values_list("role__name")
        .annotate(
            name=Concat("person__first_name", Value(" "), "person__last_name")
        )
    )
    team = defaultdict(list)
    [team[key].append(value) for key, value in qs]
    return team
