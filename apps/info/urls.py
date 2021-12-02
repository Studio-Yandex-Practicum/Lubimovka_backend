from django.urls import include, path

from apps.info.views import (
    FestivalTeamsViewSet,
    FestivalViewSet,
    PartnersViewSet,
    PressReleaseAPIView,
    QuestionCreateAPI,
    SponsorViewSet,
    VolunteersViewSet,
    festivals_years,
)
from apps.static_pages.views import StaticPagesView

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
    path(
        "press-releases/",
        PressReleaseAPIView.as_view(),
        name="press-release",
    ),
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
