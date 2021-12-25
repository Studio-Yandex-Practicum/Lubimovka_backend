from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.articles.views import BlogItemsViewSet, NewsItemsViewSet, ProjectsViewSet

router = DefaultRouter()
router.register(
    prefix="blog",
    viewset=BlogItemsViewSet,
    basename="blog_item",
)
router.register(
    prefix="news",
    viewset=NewsItemsViewSet,
    basename="news_item",
)
router.register(
    prefix="projects",
    viewset=ProjectsViewSet,
    basename="project",
)


articles_urls = [
    path("", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(articles_urls)),
]
