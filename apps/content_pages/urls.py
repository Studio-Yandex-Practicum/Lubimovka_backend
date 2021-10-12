from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.content_pages.views import ContentPageViewSet

router = DefaultRouter()

router.register(
    "content-pages",
    ContentPageViewSet,
    basename="content-pages",
)


content_pages_urls = [
    path("", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(content_pages_urls)),
]
