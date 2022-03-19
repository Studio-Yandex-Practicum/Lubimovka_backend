import os

import yadisk
from django.db.models.query import Prefetch
from django.utils import timezone

from apps.core.models import Role


def get_festival_year():
    if 7 <= timezone.now().month <= 12:
        return timezone.now().year + 1
    return timezone.now().year


def generate_upload_path(instance, filename):
    festival_year = get_festival_year()
    return f"{instance.__class__.__name__}/{festival_year}/{filename}"


def get_team_roles(obj, filters: dict = None):
    """Return all roles used in event.

    Collects persons related with role using Prefetch.
    """
    roles = Role.objects.filter(**filters).distinct()
    team = obj.team_members.all()
    return roles.prefetch_related(Prefetch("team_members", team))


def yandex_disk_export(y, instance):
    cwd = str(os.getcwd())
    name = str(instance.file).split("/")[-1]
    name = name.replace("\\", "_").replace("/", "_")
    try:
        y.mkdir(f"/{str(instance.year)}")
    except yadisk.exceptions.PathExistsError:
        pass
    to_dir = f"/{str(instance.year)}/{name}"
    from_dir = cwd.replace("\\", "/") + "/media/" + str(instance.file)
    try:
        y.upload(from_dir, to_dir)
    except yadisk.exceptions.PathExistsError:
        pass
    print(y.exists(f"/{str(instance.year)}"))
    print(y.copy(f"/{str(instance.year)}"))
