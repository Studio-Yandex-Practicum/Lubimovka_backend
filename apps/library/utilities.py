from django.db.models.query import Prefetch
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe

from apps.core.models import Role
from apps.core.utils import create_hash


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


def get_button_preview_page(obj):
    """Set a button to view the page."""
    item = {
        "Performance": "performance",
        "Project": "project",
        "BlogItem": "blog",
        "NewsItem": "news",
    }
    word = item[obj.get_class_name()]
    preview_page_hash = create_hash(obj.id)
    preview_link = reverse(
        f"{word}-item-detail-preview",
        kwargs={
            "id": obj.id,
            "hash": preview_page_hash,
        },
    )
    label_button = "Предпросмотр"
    if obj.status and obj.status == "PUBLISHED":
        label_button = "Просмотр"
    return mark_safe(f'<a class="button" href={preview_link}>{label_button}</a>')
