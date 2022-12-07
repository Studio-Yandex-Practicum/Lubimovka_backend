from rest_framework import serializers

from apps.library.models import Author, OtherLink, SocialNetworkLink
from apps.library.serializers import AuthorOtherPlaySerializer, AuthorPlaySerializer


class OtherLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherLink
        fields = (
            "name",
            "link",
            "is_pinned",
        )


class SocialNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetworkLink
        fields = (
            "name",
            "link",
        )


class AchievementSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    year = serializers.IntegerField(source="plays__festival__year", read_only=True)


class AuthorRetrieveSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(source="person", slug_field="full_name", read_only=True)
    city = serializers.SlugRelatedField(source="person", slug_field="city", read_only=True)
    social_networks = SocialNetworkSerializer(many=True)
    email = serializers.SlugRelatedField(source="person", slug_field="email", read_only=True)
    other_links = OtherLinkSerializer(many=True)
    plays = AuthorPlaySerializer(source="author_plays", many=True)
    other_plays = AuthorOtherPlaySerializer(many=True)
    image = serializers.ImageField()
    achievements = AchievementSerializer(many=True)

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
            "other_plays",
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

    def get_first_letter(self, obj) -> str:
        if not obj.person.last_name:
            return obj.person.first_name[0].upper()
        return obj.person.last_name[0].upper()

    class Meta:
        model = Author
        fields = (
            "slug",
            "name",
            "first_letter",
        )


class AuthorLettersSerializer(serializers.Serializer):
    letters = serializers.ListField(child=serializers.CharField())
