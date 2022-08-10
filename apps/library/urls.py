from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.library.views import (
    AuthorLettersAPIView,
    AuthorsReadViewSet,
    PlayFiltersAPIView,
    PlayViewSet,
    SearchResultViewSet,
    slug_determine,
)

router = DefaultRouter()
router.register(
    "plays",
    PlayViewSet,
    basename="plays",
)
router.register(
    "search",
    SearchResultViewSet,
    basename="search",
)
router.register(
    "authors",
    AuthorsReadViewSet,
    basename="authors",
)

library_urls = [
    path("library/", include(router.urls)),
    path(
        "library/author_letters/",
        AuthorLettersAPIView.as_view(),
        name="author_letters",
    ),
    path(
        "library/playfilters/",
        PlayFiltersAPIView.as_view(),
        name="playfilters",
    ),
    path(
        "library/<str:identifier>/",
        slug_determine,
        name="slug_determine",
    ),
]

urlpatterns = [
    path("v1/", include(library_urls)),
]
