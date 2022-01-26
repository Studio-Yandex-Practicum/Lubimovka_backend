from django.urls import include, path

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
from apps.static_pages.views import StaticPagesView

press_release = PressReleaseViewSet.as_view({"get": "retrieve"})
press_release_years = PressReleaseViewSet.as_view({"get": "get_press_release_years"})
press_release_download = PressReleaseViewSet.as_view({"get": "download_press_release"})


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
    path(
        "<slug:static_page_url>/",
        StaticPagesView.as_view(),
        name="static_page",
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
    path(
        "press-releases/<int:festival__year>/",
        press_release,
        name="press-releases",
    ),
    path(
        "press-releases/years/",
        press_release_years,
        name="press-releases_years",
    ),
    path(
        "press-releases/<int:festival__year>/download/",
        press_release_download,
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
