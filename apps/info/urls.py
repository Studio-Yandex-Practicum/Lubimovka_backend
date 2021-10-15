from django.urls import include, path

from apps.info.views import PartnersViewSet, QuestionCreateAPI

# from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(
#     "organizers",
#     # PartnersAPIView,
#     basename="organizers",
# )

# festival_urls = [
#     path("", include(router.urls)),
#     path("what-we-do/"),
#     path("sponsors/"),
#     path("ideology/"),
# ]

info_urls = [
    # path("about-festival/", include(festival_urls)),
    path("partners/", PartnersViewSet.as_view(), name="partners"),
    path("questions/", QuestionCreateAPI.as_view(), name="questions"),
]

urlpatterns = [
    path("v1/", include(info_urls)),
]
