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
from apps.articles.views.news_items import PreviewNewsItemDetailViewSet
from apps.articles.views.projects import PreviewProjectsDetailAPI

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
    path(
        route="preview/<int:id>/<str:hash>/",
        view=BlogItemDetailAPI.as_view(),
        name="blog-item-detail-preview",
    ),
]

news_item_urls = [
    path(route="years-months/", view=NewsItemYearsMonthsAPI.as_view(), name="news-item-years-months"),
    path(
        route="preview/<int:pk>/<str:hash>/",
        view=PreviewNewsItemDetailViewSet.as_view({"get": "retrieve"}),
        name="news-item-detail-preview",
    ),
]

articles_urls = [
    path("blog/", include(blog_item_urls)),
    path("news/", include(news_item_urls)),
    path("", include(router.urls)),
    path(
        route="project/preview/<int:id>/<str:hash>/",
        view=PreviewProjectsDetailAPI.as_view(),
        name="project-item-detail-preview",
    ),
]

urlpatterns = [
    path("v1/", include(articles_urls)),
]
