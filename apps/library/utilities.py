from django.contrib.admin.widgets import AutocompleteSelect
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


class CustomAutocompleteSelect(AutocompleteSelect):
    def __init__(self, field, admin_site, attrs=None, choices=(), using=None, placeholder=None):
        AutocompleteSelect.__init__(self, field, admin_site, attrs=None, choices=(), using=None)
        self.placeholder = placeholder

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs.update(
            {
                "data-allow-clear": "true",
                "data-dropdown-auto-width": "true",
                "data-placeholder": self.placeholder,
            }
        )
        return attrs
