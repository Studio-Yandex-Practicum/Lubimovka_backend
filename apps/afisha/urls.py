from django.urls import include, path

from apps.afisha.views import EventsAPIView

afisha_urls = [
    path("afisha/events/", EventsAPIView.as_view(), name="events"),
]

urlpatterns = [
    path("v1/", include(afisha_urls)),
]
