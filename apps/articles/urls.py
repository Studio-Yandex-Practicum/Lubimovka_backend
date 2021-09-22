from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.articles.views import BlogAPIView, NewsAPIView, ProjectsAPIView

router = DefaultRouter()
router.register(
    "news",
    NewsAPIView,
    basename="news",
)
router.register(
    "blog",
    BlogAPIView,
    basename="blog",
)
router.register(
    "projects",
    ProjectsAPIView,
    basename="projects",
)


articles_urls = [
    path("", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(articles_urls)),
]
