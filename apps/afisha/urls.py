from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.afisha.views import AfishaEventListAPIView, AfishaInfoAPIView, PerformancePreviewDetailAPI, PerformanceViewSet

router = DefaultRouter()
router.register(
    "performances",
    PerformanceViewSet,
    basename="performance",
)

performance_item_urls = [
    path("", include(router.urls)),
    path(
        route="performances/<int:id>/preview/",
        view=PerformancePreviewDetailAPI.as_view(),
        name="performance-detail-preview",
    ),
]


afisha_urls = [
    path("events/", AfishaEventListAPIView.as_view(), name="afisha-event-list"),
    path("info/", AfishaInfoAPIView.as_view(), name="afisha-info"),
]

urlpatterns = [
    path("v1/afisha/", include(performance_item_urls)),
    path("v1/afisha/", include(afisha_urls)),
]
