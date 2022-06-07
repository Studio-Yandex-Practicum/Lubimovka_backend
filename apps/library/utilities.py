from django.db.models.query import Prefetch

from apps.core.constants import YOUTUBE_VIDEO_LINKS
from apps.core.models import Role
from apps.library.models import Play


def get_team_roles(obj, filters: dict = None):
    """Return all roles used in event.

    Collects persons related with role using Prefetch.
    """
    roles = Role.objects.filter(**filters).distinct()
    team = obj.team_members.all()
    return roles.prefetch_related(Prefetch("team_members", team))


def get_video_links():
    used_links = Play.objects.filter(other_play=False).values_list("url_reading", flat=True)
    video_links = []
    for link in YOUTUBE_VIDEO_LINKS:
        if link not in used_links:
            video_links.append(link)
            video_links.append(None)
    return video_links
