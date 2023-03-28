from pathlib import Path
from typing import TypeVar, Union, overload

from django.contrib.auth import get_user_model
from django.db.models.fields.files import ImageFieldFile
from django.utils import timezone

from apps.articles.models import BlogItem, BlogPerson
from apps.articles.models.news_items import NewsItem
from apps.articles.models.projects import Project
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
from apps.core.constants import Status

COPY_TITLE = "Копия {original_title}"
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


def duplicate_image(image: ImageFieldFile):
    image.save(Path(image.name).name, image, False)


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


ArticleItem = TypeVar("ArticleItem", BlogItem, NewsItem, Project)


@overload
def article_item_copy(article_item: BlogItem, creator: User) -> BlogItem:
    ...


@overload
def article_item_copy(article_item: NewsItem, creator: User) -> NewsItem:
    ...


@overload
def article_item_copy(article_item: Project, creator: User) -> Project:
    ...


def article_item_copy(article_item: ArticleItem, creator: User) -> ArticleItem:
    article_contents = article_item.contents.all()
    bool(article_contents)  # executes the query
    source_article_pk = article_item.pk
    article_item.pk = None
    article_item.pub_date = timezone.now()
    article_item.title = COPY_TITLE.format(original_title=article_item.title)
    article_item.status = Status.IN_PROCESS
    article_item.creator = creator
    duplicate_image(article_item.image)
    article_item.save()
    if isinstance(article_item, BlogItem):
        blog_persons = BlogPerson.objects.filter(blog_id=source_article_pk)
        for blog_person in blog_persons:
            blog_person.pk = None
            blog_person.blog = article_item
            blog_person.save()
    for article_content in article_contents:
        article_content.pk = None
        article_content.content_page = article_item
        ContentModel = article_content.content_type.model_class()
        content = ContentModel.objects.get(pk=article_content.object_id)
        block_copy = content_block_copy(content)
        article_content.object_id = block_copy.pk
        article_content.save()
    return article_item
