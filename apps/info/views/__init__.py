from apps.info.views.contacts import ContactsAPIView

from .festival import FestivalAPIView, FestivalYearsAPIView
from .festivalteams import FestivalTeamsAPIView
from .partners import PartnersAPIView
from .press_release import PressReleaseDownloadAPIView, PressReleaseViewSet, PressReleaseYearsAPIView
from .question import QuestionCreateAPIView
from .sponsors import SponsorsAPIView
from .volunteers import VolunteersAPIView

__all__ = (
    FestivalAPIView,
    FestivalTeamsAPIView,
    FestivalYearsAPIView,
    PartnersAPIView,
    QuestionCreateAPIView,
    PressReleaseViewSet,
    PressReleaseYearsAPIView,
    PressReleaseDownloadAPIView,
    SponsorsAPIView,
    VolunteersAPIView,
    ContactsAPIView,
)
