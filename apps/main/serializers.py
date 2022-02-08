from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from apps.afisha.serializers import EventSerializerRegular
from apps.articles.serializers import BlogItemListSerializer, NewsItemListSerializer
from apps.info.serializers.place import PlaceSerializer
from apps.library.serializers import PlaySerializer
from apps.main.models import Banner
from apps.main.schema.schema_extension import MAIN_SCHEMA_SUCCESS_MESSAGE


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        exclude = (
            "created",
            "modified",
        )


class MainAfishaSerializer(serializers.Serializer):
    """Returns title and items for `afisha` block on main page.

    items: depending on the settings, it returns events for today or for 6 upcoming events.

    """

    afisha_today = serializers.BooleanField(default=False)
    description = serializers.CharField()
    items = EventSerializerRegular(many=True)


class MainBannersSerializer(serializers.Serializer):
    """Returns items for `banners` block on main page.

    items: returns all `Banner` items. It's impossible to have more than three
    banners.
    """

    items = BannerSerializer(many=True)


class MainBlogSerializer(serializers.Serializer):
    """Returns title and items for `blog` block on main page.

    items: returns 6 last published `NewsItem` objects.
    """

    title = serializers.CharField()
    items = BlogItemListSerializer(many=True)


class MainFirstScreenSerializer(serializers.Serializer):
    """Returns attributes for `first_screen` block on main page."""

    title = serializers.CharField()
    url_title = serializers.CharField()
    url = serializers.URLField()
    image = serializers.ImageField()


class MainNewsSerializer(serializers.Serializer):
    """Returns title and items for `news` block on main page.

    items: returns 6 last published `BlogItem` objects.
    """

    title = serializers.CharField()
    items = NewsItemListSerializer(many=True)


class MainPlacesSerializer(serializers.Serializer):
    """Returns items for `places` block on main page.

    items: returns all `Place` items.
    """

    items = PlaceSerializer(many=True)


class MainShortListSerializer(serializers.Serializer):
    """Returns title and items for `short_list` block on main page.

    items: returns 4 last `Play` objects that have program="short_list" from
    the last festival.
    """

    title = serializers.CharField()
    items = PlaySerializer(many=True)


class MainVideoArchiveSerializer(serializers.Serializer):
    """Returns attributes for `video_archive` block on main page."""

    url = serializers.URLField()
    photo = serializers.ImageField()


@extend_schema_serializer(
    OpenApiExample(
        name="Schema for main",
        value=MAIN_SCHEMA_SUCCESS_MESSAGE,
        response_only=True,
    ),
)
class MainSerializer(serializers.Serializer):
    first_screen = MainFirstScreenSerializer(required=False)
    blog = MainBlogSerializer(required=False)
    news = MainNewsSerializer(required=False)
    afisha = MainAfishaSerializer(required=False)
    banners = MainBannersSerializer(required=False)
    short_list = MainShortListSerializer(required=False)
    places = MainPlacesSerializer(required=False)
    video_archive = MainVideoArchiveSerializer(required=False)
