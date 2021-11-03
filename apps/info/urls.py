from django.urls import include, path

from apps.info.views import (
    FestivalTeamsViewSet,
    FestivalViewSet,
    PartnersViewSet,
    QuestionCreateAPI,
    SponsorViewSet,
    VolunteersViewSet,
)
from apps.static_pages.views import StaticPagesView

about_festival_urls = [
    path(
        "<slug:static_page_url>/",
        StaticPagesView.as_view(),
        name="static_page",
    ),
    path(
        "festival-teams/",
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
]

info_urls = [
    path(
        "festival/",
        FestivalViewSet.as_view(),
        name="festival",
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
