from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from apps.articles.views import BlogItemDetailAPI, BlogItemListAPI, NewsItemsViewSet, ProjectsViewSet
from apps.articles.views.blog_items import blog_status
from apps.articles.views.news_items import news_status
from apps.articles.views.projects import project_status

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
    re_path(r"^blog_status/(?P<object_pk>\d+)/(?P<status_pk>\d+)$", blog_status, name="blog_status"),
    re_path(r"^news_status/(?P<object_pk>\d+)/(?P<status_pk>\d+)$", news_status, name="news_status"),
    re_path(r"^project_status/(?P<object_pk>\d+)/(?P<status_pk>\d+)$", project_status, name="project_status"),
]
