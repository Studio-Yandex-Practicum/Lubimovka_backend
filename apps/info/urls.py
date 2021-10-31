from django.urls import include, path

from apps.info.views import (
    FestivalTeamsViewSet,
    IdeologyViewSet,
    PartnersViewSet,
    QuestionCreateAPI,
    SponsorViewSet,
    VolunteersViewSet,
    WhatWeDoViewSet,
)

about_festival_urls = [
    path(
        "what-we-do/",
        WhatWeDoViewSet.as_view(),
        name="what-we-do",
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
    path(
        "ideology/",
        IdeologyViewSet.as_view(),
        name="ideology",
    ),
]

info_urls = [
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
