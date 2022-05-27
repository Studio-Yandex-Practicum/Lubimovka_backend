import factory
from django.contrib.contenttypes.models import ContentType

from apps.afisha.models import Event
from apps.content_pages.factories import (  # ContentUnitRichTextFactory,; LinkFactory,
    ContentUnitRichTextFactory,
    EventsBlockFactory,
    ImagesBlockFactory,
    LinkFactory,
    PersonsBlockFactory,
    PlaysBlockFactory,
    VideosBlockFactory,
)

# from apps.content_pages.factories import ContentUnitRichTextFactory, LinkFactory
from apps.content_pages.models import AbstractContent
from apps.core.decorators import restrict_factory
from apps.core.models import Person, Role
from apps.library.models import Play


@restrict_factory(
    array_event=(Event,),
    array_person=(Person, Role),
    array_play=(Play,),
)
class AbstractContentFactory(factory.django.DjangoModelFactory):
    """Abstract class for `ContentModule`."""

    class Meta:
        model = AbstractContent
        abstract = True

    class Params:
        array_image = factory.Trait(item=factory.SubFactory(ImagesBlockFactory))
        array_person = factory.Trait(item=factory.SubFactory(PersonsBlockFactory))
        array_event = factory.Trait(item=factory.SubFactory(EventsBlockFactory))
        array_play = factory.Trait(item=factory.SubFactory(PlaysBlockFactory))
        array_video = factory.Trait(item=factory.SubFactory(VideosBlockFactory))
        unit_link = factory.Trait(item=factory.SubFactory(LinkFactory))
        unit_rich_text = factory.Trait(item=factory.SubFactory(ContentUnitRichTextFactory))

    content_page = None
    item = None
    content_type = factory.LazyAttribute(lambda obj: ContentType.objects.get_for_model(obj.item))
    object_id = factory.SelfAttribute("item.id")
    order = factory.Sequence(lambda n_iterator: n_iterator)
