from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.info.views import (
    FestivalTeamsViewSet,
    FestivalViewSet,
    PartnersViewSet,
    PressReleaseViewSet,
    QuestionCreateAPI,
    SponsorViewSet,
    VolunteersViewSet,
    festivals_years,
)
from apps.static_pages.views import StaticPagesView

router = DefaultRouter()
router.register("", PressReleaseViewSet, basename="press_release")


about_festival_urls = [
    path(
        "team/",
        FestivalTeamsViewSet.as_view(),
        name="festival-teams",
    ),
    path(
        "sponsors/",
        SponsorViewSet.as_view(),
        name="sponsors",
    ),
    path(
        "volunteers/",
        VolunteersViewSet.as_view(),
        name="volunteers",
    ),
    path(
        "<slug:static_page_url>/",
        StaticPagesView.as_view(),
        name="static_page",
    ),
]

info_urls = [
    path(
        "festivals/years/",
        festivals_years,
        name="festivals_years",
    ),
    path(
        "festivals/<int:year>/",
        FestivalViewSet.as_view(),
        name="festivals",
    ),
    path(
        "about-festival/",
        include(about_festival_urls),
    ),
    path(
        "partners/",
        PartnersViewSet.as_view(),
        name="partners",
    ),
    path(
        "questions/",
        QuestionCreateAPI.as_view(),
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
