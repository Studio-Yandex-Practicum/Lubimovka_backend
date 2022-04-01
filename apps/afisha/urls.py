from django.urls import include, path

from apps.afisha.views import AfishaEventListAPIView, AfishaInfoAPIView, GetCommonEventsAdmin

afisha_urls = [
    path("afisha/events/", AfishaEventListAPIView.as_view(), name="afisha-event-list"),
    path("afisha/info/", AfishaInfoAPIView.as_view(), name="afisha-info"),
    path("afisha/get-common-events-admin/", GetCommonEventsAdmin.as_view(), name="common-events-admin"),
]

urlpatterns = [
    path("v1/", include(afisha_urls)),
]
