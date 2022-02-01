from django.urls import include, path

from apps.info.views import (
    ContactsAPIView,
    FestivalAPIView,
    FestivalTeamsAPIView,
    FestivalYearsAPIView,
    PartnersAPIView,
    PressReleaseDownloadAPIView,
    PressReleaseViewSet,
    PressReleaseYearsAPIView,
    QuestionCreateAPIView,
    SponsorsAPIView,
    VolunteersAPIView,
)

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
        "contacts/",
        ContactsAPIView.as_view(),
        name="contacts",
    ),
    path(
        "questions/",
        QuestionCreateAPIView.as_view(),
        name="questions",
    ),
    path(
        "press-releases/<int:festival__year>/",
        PressReleaseViewSet.as_view({"get": "retrieve"}),
        name="press-releases",
    ),
    path(
        "press-releases/years/",
        PressReleaseYearsAPIView.as_view(),
        name="press-releases_years",
    ),
    path(
        "press-releases/<int:festival__year>/download/",
        PressReleaseDownloadAPIView.as_view(),
        name="press-releases_download",
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
