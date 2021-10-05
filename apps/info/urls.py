from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from apps.info.views import PartnersAPIView, QuestionsAPIView

router = DefaultRouter()
router.register(
    "organizers",
    # PartnersAPIView,
    basename="organizers",
)

festival_urls = [
    path("", include(router.urls)),
    path("what-we-do/"),
    path("sponsors/"),
    path("ideology/"),
]

info_urls = [
    path("about-festival/", include(festival_urls)),
    path("partners/"),
]

urlpatterns = [
    path("v1/", include(info_urls)),
]

# from django.urls import path
# from django.urls.conf import include
# from rest_framework.routers import DefaultRouter

# from bbbs.rights.views import RightTagList, RightViewSet

# router = DefaultRouter()
# router.register("rights", RightViewSet, basename="rights")

# rights_urls = [
#     path("rights/tags/", RightTagList.as_view(), name="right-tags"),
#     path("", include(router.urls)),
# ]

# urlpatterns = [
#     path("v1/", include(rights_urls)),
# ]
