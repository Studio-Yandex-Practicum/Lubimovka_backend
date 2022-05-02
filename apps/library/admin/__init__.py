from django.contrib import admin
from django.contrib.sites.models import Site

from .author import AuthorAdmin
from .events import MasterClassAdmin, PerformanceAdmin, ReadingAdmin
from .performancemediareview import PerformanceMediaReviewAdmin
from .performancereview import PerformanceReviewAdmin
from .play import PlayAdmin
from .programtype import ProgramTypeAdmin

__all__ = (
    AuthorAdmin,
    MasterClassAdmin,
    PerformanceAdmin,
    PerformanceMediaReviewAdmin,
    PerformanceReviewAdmin,
    PlayAdmin,
    ProgramTypeAdmin,
    ReadingAdmin,
)

admin.site.unregister(Site)
