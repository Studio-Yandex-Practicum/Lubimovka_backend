from rest_framework import serializers

from .author import AuthorListSerializer
from .play import PlaySerializer

# from apps.library.models import Author, Play


class SearchResultSerializer(serializers.Serializer):
    plays = PlaySerializer()
    authors = AuthorListSerializer()
