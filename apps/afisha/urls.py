from django.urls import include, path

from apps.afisha.views import AfishaFestivalStatusAPIView, EventsAPIView

afisha_urls = [
    path("afisha/events/", EventsAPIView.as_view(), name="events"),
    path("afisha/festival-status/", AfishaFestivalStatusAPIView.as_view(), name="afisha-festival-status"),
]

urlpatterns = [
    path("v1/", include(afisha_urls)),
]
