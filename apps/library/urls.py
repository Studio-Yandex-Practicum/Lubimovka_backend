from django.urls import include, path

from apps.library.views import ParticipationAPIView

paths = [
    path(
        "participation",
        ParticipationAPIView.as_view(),
        name="participation",
    ),
]

library_urls = [
    path("library/", include(paths)),
]

urlpatterns = [
    path("v1/", include(library_urls)),
]
