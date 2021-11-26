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
    roles = serializers.SerializerMethodField()

    def get_other_blogs(self, obj):
        """Returns latest four `BlogItem` except the object itself."""
        latest_four_blogs_qs = BlogItem.objects.exclude(id=obj.id)[:4]
        serializer = BlogItemBaseSerializer(
            instance=latest_four_blogs_qs,
            many=True,
        )
        return serializer.data

    def get_roles(self, obj):
        """Limits roles and blog_persons, returns serialized data.

        Do three things:
            1. Limits `roles` to distinct `roles`
            2. Limits  `blog_persons` (roles reverse relation) with blog_item's
            objects only (typically `role.blog_persons` returns all
            blog_persons, not only related to exact blog_item).
            3. Returns serialized data
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
            "roles",
            "other_blogs",
        )
