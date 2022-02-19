from rest_framework import serializers

from apps.articles.models import BlogItem
from apps.core.models import Role


class RoleSerializer(serializers.ModelSerializer):

    persons = serializers.SlugRelatedField(
        source="blog_persons",
        slug_field="annotated_full_name",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Role
        fields = (
            "name",
            "slug",
            "persons",
        )


class BlogItemListSerializer(serializers.ModelSerializer):
    pub_date = serializers.DateTimeField(required=True)

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
