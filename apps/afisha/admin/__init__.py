from django.contrib import admin
from django.contrib.sites.models import Site

from apps.afisha.admin.events import EventAdmin
from apps.afisha.admin.masterclass import MasterClassAdmin
from apps.afisha.admin.performance import PerformanceAdmin, TeamMemberInline
from apps.afisha.admin.reading import ReadingAdmin
from apps.library.admin.author import AuthorAdmin

__all__ = (
    EventAdmin,
    AuthorAdmin,
    MasterClassAdmin,
    PerformanceAdmin,
    TeamMemberInline,
    ReadingAdmin,
)

admin.site.unregister(Site)
