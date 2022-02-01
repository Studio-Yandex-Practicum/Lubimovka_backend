from django.db.models.query import Prefetch
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from apps.articles.models import BlogItem
from apps.articles.schema.schema_extension import SUCCESS_MESSAGE_FOR_BLOG_ITEM_DETAIL_FOR_200
from apps.articles.services import get_latest_four_published_items_data
from apps.content_pages.serializers import BaseContentPageSerializer
from apps.core.models import Role


class RoleSerializer(serializers.ModelSerializer):

    persons = serializers.SerializerMethodField()

    def get_persons(self, obj):

        persons = []

        for team_member in obj.blog_persons.all():
            persons.append(team_member.person.full_name)
        return persons

    class Meta:
        model = Role
        fields = (
            "name",
            "slug",
            "persons",
        )


class BlogItemBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogItem
        fields = (
            "id",
            "pub_date",
            "title",
            "description",
            "author_url",
            "author_url_title",
            "image",
        )


class BlogItemListSerializer(BlogItemBaseSerializer):
    pass


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Schema for blog item detail",
            value=SUCCESS_MESSAGE_FOR_BLOG_ITEM_DETAIL_FOR_200,
            request_only=False,
            response_only=True,
        ),
    ],
)
class BlogItemDetailedSerializer(
    BaseContentPageSerializer,
    serializers.ModelSerializer,
):
    other_blogs = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()

    def get_other_blogs(self, obj):
        """Return latest four `BlogItem` except the object itself."""
        serialized_data = get_latest_four_published_items_data(
            serializer_class=BlogItemListSerializer,
            object=obj,
        )
        return serialized_data

    def get_team(self, obj):
        """Make `team` serialized data based on `roles` and `blog_persons`.

        Team serialized data has to look like this:
        "team": [
            {
                "name": "Переводчик",
                "slug": "translator",
                "persons": [
                    "Каллистрат Абрамов",
                    "Александра Авдеева"
            },
            {
                ...
            }
        ]

        To make it three things have to be done:
            1. Limit `roles` to distinct `roles`
            2. Limit (prefetch) `blog_persons` (roles reverse relation) with
            blog_item's objects only (typically `role.blog_persons` returns all
            blog_persons, not only related to exact blog_item).
            3. Return serialized data
        """
        blog_item = obj
        blog_roles = blog_item.roles.distinct()
        blog_persons = blog_item.blog_persons.all()

        blog_roles_with_limited_blog_persons = blog_roles.prefetch_related(
            Prefetch(
                "blog_persons",
                queryset=blog_persons,
            ),
        )
        serializer = RoleSerializer(
            instance=blog_roles_with_limited_blog_persons,
            many=True,
        )
        return serializer.data

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
