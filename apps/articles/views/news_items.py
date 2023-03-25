from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import filters as rest_filters
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from apps.articles import selectors
from apps.articles.filters import PubDateFilter
from apps.articles.mixins import PubDateSchemaMixin
from apps.articles.models import NewsItem
from apps.articles.serializers import NewsItemDetailSerializer, NewsItemListSerializer, YearMonthSerializer
from apps.articles.serializers.common import QueryYearMonthParamsSerializer


class NewsItemsListAPI(PubDateSchemaMixin, generics.ListAPIView):
    """Returns published News items."""

    filter_backends = (
        filters.DjangoFilterBackend,
        rest_filters.OrderingFilter,
    )
    filterset_class = PubDateFilter
    ordering_fields = (
        "pub_date__year",
        "pub_date__month",
    )
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    serializer_class = NewsItemListSerializer
    queryset = NewsItem.objects.published()

    class NewsItemListFilterSerializer(QueryYearMonthParamsSerializer):
        pass

    def get(self, request, *args, **kwargs):
        filters_serializer = self.NewsItemListFilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        return super().get(request, *args, **kwargs)


class NewsItemsDetailAPI(APIView):
    """Returns object `NewsItems`."""

    @extend_schema(responses=NewsItemDetailSerializer)
    def get(self, request, id):
        news_item_detail = selectors.item_detail_get(NewsItem, id)
        context = {"request": request}
        serializer = NewsItemDetailSerializer(news_item_detail, context=context)
        return Response(serializer.data)


class NewsItemsPreviewDetailAPI(APIView):
    """Returns preview page `NewsItems`."""

    @extend_schema(responses=NewsItemDetailSerializer)
    def get(self, request, id):
        hash_sum = request.GET.get("hash", None)
        item_detail = selectors.preview_item_detail_get(NewsItem, id, hash_sum)
        news_item_detail = selectors.item_detail_get(NewsItem, id, item_detail)
        context = {"request": request}
        serializer = NewsItemDetailSerializer(news_item_detail, context=context)
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
