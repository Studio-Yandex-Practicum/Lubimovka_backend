from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.articles.filters import PubDateFilter
from apps.articles.mixins import PubDateSchemaMixin
from apps.articles.models import NewsItem
from apps.articles.serializers import NewsItemDetailedSerializer, NewsItemListSerializer


def news_prev_status(request, object_pk):
    messages.info(request, "Статус успешно обновлен!")
    news = NewsItem.objects.get(pk=object_pk)
    news.status = news.status.prev()
    news.save()
    return HttpResponseRedirect(reverse("admin:articles_newsitem_change", args=[object_pk]))


def news_next_status(request, object_pk):
    messages.info(request, "Статус успешно обновлен!")
    news = NewsItem.objects.get(pk=object_pk)
    news.status = news.status.next()
    news.save()
    return HttpResponseRedirect(reverse("admin:articles_newsitem_change", args=[object_pk]))


class NewsItemsViewSet(PubDateSchemaMixin, ReadOnlyModelViewSet):
    """Returns published News items."""

    queryset = NewsItem.ext_objects.published()
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    )
    filterset_class = PubDateFilter
    ordering_fields = (
        "pub_date__year",
        "pub_date__month",
    )

    def get_serializer_class(self):
        if self.action == "list":
            return NewsItemListSerializer
        return NewsItemDetailedSerializer

    class Meta:
        model = NewsItem
