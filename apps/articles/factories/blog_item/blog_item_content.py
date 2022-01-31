import factory

from apps.content_pages.tests.factories import (
    AbstractContentFactory,
    ImagesBlockFactory,
    PersonsBlockFactory,
    PlaysBlockFactory,
    PreambleFactory,
    QuoteFactory,
    TextFactory,
    TitleFactory,
)

from ...models import BlogItem, BlogItemContent


class AbstractBlogItemContentFactory(AbstractContentFactory):
    """Base content factory for `BlogItem`.

    1. It set relation with `BlogItem` object.
    2. It inherits generic relations with `content_items` form `AbstractContentFactory`
    """

    class Meta:
        model = BlogItemContent
        exclude = ("item",)
        abstract = True

    content_page = factory.Iterator(BlogItem.objects.all())


class BlogItemImagesBlockContentFactory(AbstractBlogItemContentFactory):
    item = factory.SubFactory(ImagesBlockFactory)


class BlogItemPersonsBlockContentFactory(AbstractBlogItemContentFactory):
    item = factory.SubFactory(PersonsBlockFactory)


class BlogItemPlaysBlockContentFactory(AbstractBlogItemContentFactory):
    item = factory.SubFactory(PlaysBlockFactory)


class BlogItemPreambleContentFactory(AbstractBlogItemContentFactory):
    class Meta:
        model = BlogItemContent

    item = factory.SubFactory(PreambleFactory)
    content_page = factory.Iterator(BlogItem.objects.all())


class BlogItemQuoteContentFactory(AbstractBlogItemContentFactory):
    item = factory.SubFactory(QuoteFactory)


class BlogItemTextContentFactory(AbstractBlogItemContentFactory):
    item = factory.SubFactory(TextFactory)


class BlogItemTitleContentFactory(AbstractBlogItemContentFactory):
    item = factory.SubFactory(TitleFactory)
