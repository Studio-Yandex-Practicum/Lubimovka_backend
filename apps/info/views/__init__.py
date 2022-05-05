from apps.info.views.contacts import ContactsAPIView

from .festival import FestivalAPIView, FestivalYearsAPIView
from .festivalteams import FestivalTeamsAPIView
from .partners import PartnerListAPIView
from .press_release import PressReleaseDownloadAPIView, PressReleaseViewSet, PressReleaseYearsAPIView
from .selectors import SelectorsAPIView
from .settings import SettingsAPIView
from .sponsors import SponsorsAPIView
from .volunteers import VolunteersAPIView

__all__ = (
    FestivalAPIView,
    FestivalTeamsAPIView,
    FestivalYearsAPIView,
    PartnerListAPIView,
    PressReleaseViewSet,
    PressReleaseYearsAPIView,
    PressReleaseDownloadAPIView,
    SponsorsAPIView,
    VolunteersAPIView,
    ContactsAPIView,
    SettingsAPIView,
    SelectorsAPIView,
)
