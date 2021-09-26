from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.afisha.views import EventsAPIView

router = DefaultRouter()
router.register(
    "events",
    EventsAPIView,
    basename="events",
)


afisha_urls = [
    path("afisha/", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(afisha_urls)),
]
