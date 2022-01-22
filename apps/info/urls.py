from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.info.views import (
    FestivalAPIView,
    FestivalTeamsAPIView,
    FestivalYearsAPIView,
    PartnersAPIView,
    PressReleaseViewSet,
    QuestionCreateAPIView,
    SponsorsAPIView,
    VolunteersAPIView,
)

router = DefaultRouter()
router.register("", PressReleaseViewSet, basename="press_release")


about_festival_urls = [
    path(
        "team/",
        FestivalTeamsAPIView.as_view(),
        name="festival-teams",
    ),
    path(
        "sponsors/",
        SponsorsAPIView.as_view(),
        name="sponsors",
    ),
    path(
        "volunteers/",
        VolunteersAPIView.as_view(),
        name="volunteers",
    ),
]

info_urls = [
    path(
        "festivals/years/",
        FestivalYearsAPIView.as_view(),
        name="festivals-years",
    ),
    path(
        "festivals/<int:year>/",
        FestivalAPIView.as_view(),
        name="festivals",
    ),
    path(
        "about-festival/",
        include(about_festival_urls),
    ),
    path(
        "partners/",
        PartnersAPIView.as_view(),
        name="partners",
    ),
    path(
        "questions/",
        QuestionCreateAPIView.as_view(),
        name="questions",
    ),
    path("press-releases/", include(router.urls)),
]

app_prefix = [
    path(
        "info/",
        include(info_urls),
    )
]

urlpatterns = [
    path(
        "v1/",
        include(app_prefix),
    ),
]
