from rest_framework import serializers

from apps.library.models import Author, OtherLink, SocialNetworkLink

from .play import PlaySerializer


class OtherLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherLink
        fields = (
            "name",
            "link",
            "is_pinned",
            "order_number",
        )


class SocialNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetworkLink
        fields = (
            "name",
            "link",
        )


class AuthorRetrieveSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(source="person", slug_field="full_name", read_only=True)
    city = serializers.SlugRelatedField(source="person", slug_field="city", read_only=True)
    achievements = serializers.SlugRelatedField(slug_field="tag", read_only=True, many=True)
    social_networks = SocialNetworkSerializer(many=True)
    email = serializers.SlugRelatedField(source="person", slug_field="email", read_only=True)
    other_links = OtherLinkSerializer(many=True)
    plays = PlaySerializer(many=True)
    image = serializers.ImageField()

    class Meta:
        model = Author
        fields = (
            "slug",
            "name",
            "city",
            "quote",
            "biography",
            "achievements",
            "social_networks",
            "email",
            "other_links",
            "plays",
            "image",
        )


class AuthorListSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(source="person", slug_field="reversed_full_name", read_only=True)

    class Meta:
        model = Author
        fields = (
            "slug",
            "name",
        )


class AuthorSearchSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(
        source="person",
        slug_field="reversed_full_name",
        read_only=True,
    )
    first_letter = serializers.SerializerMethodField()

    def get_first_letter(self, obj):
        return obj.person.last_name[0].upper()

    class Meta:
        model = Author
        fields = (
            "slug",
            "name",
            "first_letter",
        )
