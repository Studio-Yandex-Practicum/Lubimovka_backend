from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.articles.views import (
    BlogItemDetailAPI,
    BlogItemListAPI,
    BlogItemPreviewDetailAPI,
    BlogItemYearsMonthsAPI,
    NewsItemsPreviewDetailAPI,
    NewsItemsViewSet,
    NewsItemYearsMonthsAPI,
    ProjectDetailAPI,
    ProjectListAPI,
    ProjectsPreviewDetailAPI,
)

router = DefaultRouter()
router.register(
    prefix="news",
    viewset=NewsItemsViewSet,
    basename="news-item",
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
        route="<int:id>/preview/",
        view=NewsItemsPreviewDetailAPI.as_view(),
        name="news-item-detail-preview",
    ),
]

project_item_urls = [
    path(
        route="",
        view=ProjectListAPI.as_view(),
        name="project-list",
    ),
    path(
        route="<int:id>/",
        view=ProjectDetailAPI.as_view(),
        name="project-detail",
    ),
    path(
        route="<int:id>/preview/",
        view=ProjectsPreviewDetailAPI.as_view(),
        name="project-detail-preview",
    ),
]

articles_urls = [
    path("blog/", include(blog_item_urls)),
    path("news/", include(news_item_urls)),
    path("projects/", include(project_item_urls)),
    path("", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(articles_urls)),
]
