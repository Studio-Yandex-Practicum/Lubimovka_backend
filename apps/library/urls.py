from django.urls import include, path

from apps.library.views import ParticipationCreateAPI

paths = [
    path(
        "participation",
        ParticipationCreateAPI.as_view(),
        name="participation",
    ),
]

library_urls = [
    path("library/", include(paths)),
]

urlpatterns = [
    path("v1/", include(library_urls)),
]
