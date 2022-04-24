from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.articles.views import (
    BlogItemDetailAPI,
    BlogItemListAPI,
    BlogItemYearsMonthsAPI,
    NewsItemsViewSet,
    NewsItemYearsMonthsAPI,
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

blog_item_urls = [
    path(route="", view=BlogItemListAPI.as_view(), name="blog-item-list"),
    path(route="years-months/", view=BlogItemYearsMonthsAPI.as_view(), name="blog-item-years-months"),
    path(route="<int:id>/", view=BlogItemDetailAPI.as_view(), name="blog-item-detail"),
]

articles_urls = [
    path("blog/", include(blog_item_urls)),
    path(route="news/years-months/", view=NewsItemYearsMonthsAPI.as_view(), name="news-item-years-months"),
    path("", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(articles_urls)),
]
