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
    ProjectsPreviewDetailAPI,
    ProjectsViewSet,
)

router = DefaultRouter()
router.register(
    prefix="news",
    viewset=NewsItemsViewSet,
    basename="news-item",
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
    path(
        route="<int:id>/preview/",
        view=BlogItemPreviewDetailAPI.as_view(),
        # don't change name, look PreviewButtonMixin
        name="blogitem-detail-preview",
    ),
]

news_item_urls = [
    path(route="years-months/", view=NewsItemYearsMonthsAPI.as_view(), name="news-item-years-months"),
    path(
        route="<int:id>/preview/",
        view=NewsItemsPreviewDetailAPI.as_view(),
        # don't change name, look PreviewButtonMixin
        name="newsitem-detail-preview",
    ),
]

project_item_urls = [
    path(
        route="<int:id>/preview/",
        view=ProjectsPreviewDetailAPI.as_view(),
        # don't change name, look PreviewButtonMixin
        name="project-detail-preview",
    )
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
