from rest_framework import serializers

from apps.content_pages.models import AbstractContentPage


def get_latest_four_published_items_data(
    serializer_class: serializers.Serializer,
    object: AbstractContentPage,
) -> dict():
    """Return four latest `model` items serialized data except `object` itself."""
    model_class = object.__class__

    published_items = model_class.ext_objects.published()
    latest_four_items = published_items.exclude(id=object.id)[:4]
    serializer = serializer_class(instance=latest_four_items, many=True)
    return serializer.data
