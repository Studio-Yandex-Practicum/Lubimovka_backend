from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import filters as rest_filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.articles import selectors
from apps.articles.filters import PubDateFilter
from apps.articles.mixins import PubDateSchemaMixin
from apps.articles.models import NewsItem
from apps.articles.serializers import NewsItemDetailedSerializer, NewsItemListSerializer, YearMonthSerializer
from apps.core.utils import create_hash


class NewsItemsViewSet(PubDateSchemaMixin, ReadOnlyModelViewSet):
    """If `ingress` exist returns preview page else returns published items."""

    def get_queryset(self, **kwargs):
        object_id = self.kwargs["pk"]
        model_name = "newsitem"
        ingress = self.request.GET.get("ingress", "")
        if ingress == create_hash(object_id, model_name):
            queryset = NewsItem.ext_objects.current_and_published(object_id)
        else:
            queryset = NewsItem.ext_objects.published()
        return queryset

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


class NewsItemYearsMonthsAPI(APIView):
    """Return years and months of published `NewsItem`."""

    class NewsItemYearsMonthsOutputSerializer(YearMonthSerializer):
        pass

    @extend_schema(responses=NewsItemYearsMonthsOutputSerializer(many=True))
    def get(self, request):
        news_item_years_months = selectors.article_get_years_months_publications(NewsItem)
        serializer = self.NewsItemYearsMonthsOutputSerializer(news_item_years_months, many=True)
        return Response(serializer.data)
