from pathlib import Path
from typing import Union, overload

from django.contrib.auth import get_user_model
from django.db.models.fields.files import ImageFieldFile

from apps.content_pages.models.content_blocks import (
    ContentPersonRole,
    EventsBlock,
    ExtendedPerson,
    ImagesBlock,
    OrderedEvent,
    OrderedImage,
    OrderedPlay,
    OrderedVideo,
    PersonsBlock,
    PlaysBlock,
    VideosBlock,
)
from apps.content_pages.models.content_items import AbstractItemWithTitle, ContentUnitRichText, Link

ITEM_MODEL = {
    EventsBlock: OrderedEvent,
    ImagesBlock: OrderedImage,
    VideosBlock: OrderedVideo,
    PlaysBlock: OrderedPlay,
    PersonsBlock: ExtendedPerson,
    ContentUnitRichText: None,
    Link: None,
}

User = get_user_model()


def copy_image(source_image: ImageFieldFile, destination_image: ImageFieldFile):
    """Attach a new copy of a file attached to the source ImageField to the destination ImageField."""
    destination_image.save(Path(source_image.name).name, source_image, False)


def duplicate_image(image: ImageFieldFile):
    """Create a new copy of a file attached to the ImageField."""
    copy_image(image, image)


@overload
def content_block_copy(block: AbstractItemWithTitle) -> AbstractItemWithTitle:
    ...


@overload
def content_block_copy(block: ContentUnitRichText) -> ContentUnitRichText:
    ...


def content_block_copy(
    block: Union[AbstractItemWithTitle, ContentUnitRichText]
) -> Union[AbstractItemWithTitle, ContentUnitRichText]:
    source_block_id = block.pk
    block.pk = None
    block.save()
    ItemModel = ITEM_MODEL.get(type(block))
    # Link and ContentUnitRichText do not contain blocks
    if not hasattr(ItemModel, "block"):
        return block
    items = ItemModel.objects.filter(block_id=source_block_id)
    for item in items:
        source_item_pk = item.pk
        item.pk = None
        item.block = block
        if hasattr(item, "image"):
            duplicate_image(item.image)
        item.save()
        # ExtendedPerson has one more level of indirection handling person's roles
        if isinstance(item, ExtendedPerson):
            through_roles = ContentPersonRole.objects.filter(extended_person_id=source_item_pk)
            for through_role in through_roles:
                through_role.pk = None
                through_role.extended_person = item
                through_role.save()
    return block
