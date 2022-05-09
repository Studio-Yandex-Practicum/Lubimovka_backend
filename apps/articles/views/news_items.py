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


class NewsItemsPreviewDetailAPI(APIView):
    """Returns preview page `NewsItems`."""

    def get(self, request, id):
        hash_sum = request.GET.get("hash", None)
        news_item_detail = selectors.preview_item_detail_get(NewsItem, id, hash_sum)
        context = {"request": request}
        serializer = NewsItemDetailedSerializer(news_item_detail, context=context)
        return Response(serializer.data)


class NewsItemYearsMonthsAPI(APIView):
    """Return years and months of published `NewsItem`."""

    class NewsItemYearsMonthsOutputSerializer(YearMonthSerializer):
        pass

    @extend_schema(responses=NewsItemYearsMonthsOutputSerializer(many=True))
    def get(self, request):
        news_item_years_months = selectors.article_get_years_months_publications(NewsItem)
        serializer = self.NewsItemYearsMonthsOutputSerializer(news_item_years_months, many=True)
        return Response(serializer.data)
