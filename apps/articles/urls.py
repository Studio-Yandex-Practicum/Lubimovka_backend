from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.articles.views import BlogItemDetailAPI, BlogItemListAPI, NewsItemsViewSet, ProjectsViewSet
from apps.articles.views.articles_status import blog_status, news_status, project_status

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
]

urlpatterns = [
    path("v1/", include(articles_urls)),
    path("blog_status/<int:object_pk>/<str:status/", blog_status, name="blog_status"),
    path("news_status/<int:object_pk>/<str:status/", news_status, name="news_status"),
    path("project_status/<int:object_pk>/<str:status/", project_status, name="project_status"),
]
