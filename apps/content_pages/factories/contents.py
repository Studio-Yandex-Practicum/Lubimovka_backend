import factory
from django.contrib.contenttypes.models import ContentType

from ..models import AbstractContent


class AbstractContentFactory(factory.django.DjangoModelFactory):
    """Abstract class for base content."""

    class Meta:
        model = AbstractContent
        exclude = ("item", "content_page")
        abstract = True

    content_type = factory.LazyAttribute(lambda obj: ContentType.objects.get_for_model(obj.item))
    object_id = factory.SelfAttribute("item.id")
    order = factory.Sequence(lambda n_iterator: n_iterator)
