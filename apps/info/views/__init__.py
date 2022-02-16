from apps.info.views.contacts import ContactsAPIView

from .feedback import FeedbackAPIView
from .festival import FestivalAPIView, FestivalYearsAPIView
from .festivalteams import FestivalTeamsAPIView
from .partners import PartnersAPIView
from .press_release import (
    PressReleaseDownloadAPIView,
    PressReleasePhotoGalleryLink,
    PressReleaseViewSet,
    PressReleaseYearsAPIView,
)
from .question import QuestionCreateAPIView
from .sponsors import SponsorsAPIView
from .volunteers import VolunteersAPIView

__all__ = (
    FestivalAPIView,
    FestivalTeamsAPIView,
    FestivalYearsAPIView,
    PartnersAPIView,
    QuestionCreateAPIView,
    PressReleasePhotoGalleryLink,
    PressReleaseViewSet,
    PressReleaseYearsAPIView,
    PressReleaseDownloadAPIView,
    SponsorsAPIView,
    VolunteersAPIView,
    ContactsAPIView,
    FeedbackAPIView,
)
