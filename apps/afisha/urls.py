from django.urls import include, path

from apps.afisha.views import AfishaEventListAPIView, AfishaInfoAPIView

afisha_urls = [
    path("afisha/events/", AfishaEventListAPIView.as_view(), name="afisha-event-list"),
    path("afisha/info/", AfishaInfoAPIView.as_view(), name="afisha-info"),
]

urlpatterns = [
    path("v1/", include(afisha_urls)),
]
