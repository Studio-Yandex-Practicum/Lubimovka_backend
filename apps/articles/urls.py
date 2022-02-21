from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from apps.articles.views import BlogItemsViewSet, NewsItemsViewSet, ProjectsViewSet
from apps.articles.views.blog_items import blog_next_status, blog_prev_status
from apps.articles.views.news_items import news_next_status, news_prev_status
from apps.articles.views.projects import project_next_status, project_prev_status

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
    re_path(r"^blog_prev_status/(?P<object_pk>\d+)/$", blog_prev_status, name="blog_prev_status"),
    re_path(r"^blog_next_status/(?P<object_pk>\d+)/$", blog_next_status, name="blog_next_status"),
    re_path(r"^news_prev_status/(?P<object_pk>\d+)/$", news_prev_status, name="news_prev_status"),
    re_path(r"^news_next_status/(?P<object_pk>\d+)/$", news_next_status, name="news_next_status"),
    re_path(r"^project_prev_status/(?P<object_pk>\d+)/$", project_prev_status, name="project_prev_status"),
    re_path(r"^project_next_status/(?P<object_pk>\d+)/$", project_next_status, name="project_next_status"),
]
