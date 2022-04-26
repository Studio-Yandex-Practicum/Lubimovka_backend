from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.articles.views import BlogItemDetailAPI, BlogItemListAPI, NewsItemsViewSet, ProjectsViewSet
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

articles_urls = [
    path("", include(router.urls)),
    path(route="blog/", view=BlogItemListAPI.as_view(), name="blog-item-list"),
    path(route="blog/<int:id>/", view=BlogItemDetailAPI.as_view(), name="blog-item-detail"),
    path(
        route="blog/preview/<int:id>/<str:hash>/",
        view=BlogItemDetailAPI.as_view(),
        name="blog-item-detail-preview",
    ),
    path(
        route="news/preview/<int:pk>/<str:hash>/",
        view=PreviewNewsItemDetailViewSet.as_view({"get": "retrieve"}),
        name="news-item-detail-preview",
    ),
    path(
        route="project/preview/<int:id>/<str:hash>/",
        view=PreviewProjectsDetailAPI.as_view(),
        name="project-item-detail-preview",
    ),
]
urlpatterns = [
    path("v1/", include(articles_urls)),
]
