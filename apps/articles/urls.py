from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.articles.views import (
    BlogItemDetailAPI,
    BlogItemListAPI,
    BlogItemPreviewDetailAPI,
    BlogItemYearsMonthsAPI,
    NewsItemsDetailAPI,
    NewsItemsListAPI,
    NewsItemsPreviewDetailAPI,
    NewsItemYearsMonthsAPI,
    ProjectsPreviewDetailAPI,
    ProjectsViewSet,
)

router = DefaultRouter()
router.register(
    prefix="projects",
    viewset=ProjectsViewSet,
    basename="project",
)

blog_item_urls = [
    path(route="", view=BlogItemListAPI.as_view(), name="blog-item-list"),
    path(route="years-months/", view=BlogItemYearsMonthsAPI.as_view(), name="blog-item-years-months"),
    path(route="<int:id>/", view=BlogItemDetailAPI.as_view(), name="blog-item-detail"),
    path(
        route="<int:id>/preview/",
        view=BlogItemPreviewDetailAPI.as_view(),
        name="blog-item-detail-preview",
    ),
]

news_item_urls = [
    path(route="years-months/", view=NewsItemYearsMonthsAPI.as_view(), name="news-item-years-months"),
    path(
        route="",
        view=NewsItemsListAPI.as_view(),
        name="news-item-list",
    ),
    path(
        route="<int:id>/",
        view=NewsItemsDetailAPI.as_view(),
        name="news-item-detail",
    ),
    path(
        route="<int:id>/preview/",
        view=NewsItemsPreviewDetailAPI.as_view(),
        name="news-item-detail-preview",
    ),
]

project_item_urls = [
    path("", include(router.urls)),
    path(
        route="projects/<int:id>/preview/",
        view=ProjectsPreviewDetailAPI.as_view(),
        name="project-detail-preview",
    ),
]

articles_urls = [
    path("blog/", include(blog_item_urls)),
    path("news/", include(news_item_urls)),
    path("", include(project_item_urls)),
]

urlpatterns = [
    path("v1/", include(articles_urls)),
]
