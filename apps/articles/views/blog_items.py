from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from apps.articles import selectors
from apps.articles.models import BlogItem
from apps.articles.serializers import BlogItemListSerializer, BlogItemRoleSerializer, YearMonthSerializer
from apps.content_pages.serializers import BaseContentPageSerializer
from apps.core.utils import get_paginated_response


class BlogItemListAPI(APIView):
    """Return list BlogItem."""

    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    class BlogItemListFilterSerializer(serializers.Serializer):
        year = serializers.IntegerField(
            min_value=1970,
            max_value=timezone.now().year,
            required=False,
            help_text="Фильтр по году",
        )
        month = serializers.IntegerField(
            min_value=1,
            max_value=12,
            required=False,
            help_text="Фильтр по месяцам",
        )

    class BlogItemListOutputSerializer(BlogItemListSerializer):
        pass

    @extend_schema(
        parameters=[BlogItemListFilterSerializer],
        responses=BlogItemListOutputSerializer(many=True),
    )
    def get(self, request):
        filters_serializer = self.BlogItemListFilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        filtered_blog_items = selectors.blog_item_list_get(filters=filters_serializer.validated_data)
        return get_paginated_response(
            pagination_class=self.pagination_class,
            serializer_class=self.BlogItemListOutputSerializer,
            queryset=filtered_blog_items,
            request=request,
            view=self,
        )


class BlogItemDetailAPI(APIView):
    """Return datailed `BlogItem` object."""

    class BlogItemDetailOutputSerializer(BaseContentPageSerializer, serializers.ModelSerializer):
        other_blogs = BlogItemListSerializer(many=True, source="_other_blogs")
        team = BlogItemRoleSerializer(many=True, source="_team")
        pub_date = serializers.DateTimeField(required=True)

        class Meta:
            model = BlogItem
            fields = (
                "id",
                "title",
                "description",
                "image",
                "author_url",
                "author_url_title",
                "pub_date",
                "contents",
                "team",
                "other_blogs",
            )

    @extend_schema(responses=BlogItemDetailOutputSerializer)
    def get(self, request, id):
        blog_item_detail = selectors.blog_item_detail_get(blog_item_id=id)
        context = {"request": request}
        serializer = self.BlogItemDetailOutputSerializer(blog_item_detail, context=context)
        return Response(serializer.data)


class BlogItemYearsMonthsAPI(APIView):
    """Return years and monthes when at least one `BlogItem` published."""

    class BlogItemYearsMonthsOutputSerializer(YearMonthSerializer):
        pass

    @extend_schema(responses=BlogItemYearsMonthsOutputSerializer(many=True))
    def get(self, request):
        blog_item_years_months = selectors.article_get_years_months_publications(BlogItem)
        serializer = self.BlogItemYearsMonthsOutputSerializer(blog_item_years_months, many=True)
        return Response(serializer.data)
