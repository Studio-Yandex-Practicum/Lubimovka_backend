from django.db.models.query import Prefetch
from rest_framework import serializers

from apps.articles.models import BlogItem, BlogPerson
from apps.content_pages.serializers import BaseContentPageSerializer
from apps.core.models import Role


class BlogPersonSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        source="person",
        slug_field="id",
        read_only=True,
    )
    full_name = serializers.SlugRelatedField(
        source="person",
        slug_field="full_name",
        read_only=True,
    )

    class Meta:
        model = BlogPerson
        fields = (
            "id",
            "full_name",
        )


class RoleSerializer(serializers.ModelSerializer):
    persons = BlogPersonSerializer(
        source="blog_persons",
        read_only=True,
        many=True,
    )

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


class BlogItemDetailedSerializer(
    BaseContentPageSerializer,
    serializers.ModelSerializer,
):
    other_blogs = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()

    def get_other_blogs(self, obj):
        """Returns latest four `BlogItem` except the object itself."""
        published_blogs = BlogItem.ext_objects.published()
        latest_four_blogs_qs = published_blogs.exclude(id=obj.id)[:4]
        serializer = BlogItemBaseSerializer(
            instance=latest_four_blogs_qs,
            many=True,
        )
        return serializer.data

    def get_team(self, obj):
        """Make `team` serialized data based on `roles` and `blog_persons`.

        Team serialized data has to look like this:
        "team": [
            {
                "name": "Переводчик",
                "slug": "translator",
                "persons": [
                    {
                        "id": 6,
                        "full_name": "Творимир Алексеев"
                    },
                    {
                        "id": 47,
                        "full_name": "Раиса Авдеева"
                    }
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
