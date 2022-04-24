from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.articles.views import (
    BlogItemDetailAPI,
    BlogItemListAPI,
    BlogItemYearsMonthsAPI,
    NewsItemsViewSet,
    ProjectsViewSet,
)

router = DefaultRouter()
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
    path(route="blog/", view=BlogItemListAPI.as_view(), name="blog-item-list"),
    path(route="blog/years-months/", view=BlogItemYearsMonthsAPI.as_view(), name="blog-item-years-months"),
    path(route="blog/<int:id>/", view=BlogItemDetailAPI.as_view(), name="blog-item-detail"),
]

urlpatterns = [
    path("v1/", include(articles_urls)),
]
