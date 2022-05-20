from django.contrib import admin
from django.contrib.sites.models import Site

from apps.afisha.admin.events import EventAdmin
from apps.afisha.admin.master_class import MasterClassAdmin
from apps.afisha.admin.performance import PerformanceAdmin, TeamMemberInline
from apps.afisha.admin.performance_media_review import PerformanceMediaReviewAdmin
from apps.afisha.admin.performance_review import PerformanceReviewAdmin
from apps.afisha.admin.reading import ReadingAdmin

__all__ = (
    EventAdmin,
    MasterClassAdmin,
    PerformanceAdmin,
    TeamMemberInline,
    ReadingAdmin,
    PerformanceMediaReviewAdmin,
    PerformanceReviewAdmin,
)

admin.site.unregister(Site)
