import factory
from faker import Faker

from apps.content_pages.models import ContentUnitRichText, Link, Preamble, Quote, Text, Title

fake = Faker(locale="ru_RU")


class ContentUnitRichTextFactory(factory.django.DjangoModelFactory):
    """Create RichText `content` unit.

    The factory tries to emulate the structure of CKEditor plugin content. By default
    creates string with
        - <h4>
        - <h6>
        - <p>
        - <blockquote>
        - <strong>, <em>, <a> wrapped with <p>
    tags.

    Parameters:
    1. `paragraph_only` - if True, create `rich_text` with only one <p> tag.
    2. `header_h4_only` - if True, create `rich_text` with only one <h4> tag.
    4. `header_h6_only` - if True, create `rich_text` with only one <h6> tag.
    5. `blockquote_only` - if True, create `rich_text` with only one blockquote (<blockquote> tag wraps <p>).
    """

    class Meta:
        model = ContentUnitRichText
        exclude = (
            "paragraph",
            "paragraph_bold_italic_anchor",
            "header_h4",
            "header_h6",
            "quote",
        )

    class Params:
        paragraph_only = factory.Trait(rich_text=factory.SelfAttribute(".paragraph"))
        header_h4_only = factory.Trait(rich_text=factory.SelfAttribute(".header_h4"))
        header_h6_only = factory.Trait(rich_text=factory.SelfAttribute(".header_h6"))
        blockquote_only = factory.Trait(rich_text=factory.SelfAttribute(".quote"))

    paragraph = factory.LazyFunction(lambda: f"<p>{fake.paragraph(nb_sentences=5)}</p>")
    header_h4 = factory.LazyFunction(lambda: f"<h4>{fake.text(max_nb_chars=100)}</h4>")
    header_h6 = factory.LazyFunction(lambda: f"<h6>{fake.text(max_nb_chars=250)}</h6>")
    quote = factory.LazyFunction(lambda: f"<blockquote><p>{fake.text(max_nb_chars=200)}</p></blockquote>")

    @factory.lazy_attribute
    def paragraph_bold_italic_anchor(self):
        """Make paragraph with first words bold, italic and anchor."""
        paragraph = fake.paragraph(nb_sentences=2, variable_nb_sentences=False)
        (first_word, second_word, third_word, rest) = paragraph.split(maxsplit=3)
        bold_word = f"<strong>{first_word}</strong>"
        italic_word = f"<em>{second_word}</em>"
        anchor_word = f"<a href='{fake.url()}'>{third_word}<a>"
        paragraph_with_tags = (" ").join((bold_word, italic_word, anchor_word, rest))
        return f"<p>{paragraph_with_tags}</p>"

    @factory.lazy_attribute
    def rich_text(self):
        r"""Combine blocks to string separated by `\r\n\r\n` as CKEditor do."""
        elements = (self.header_h4, self.header_h6, self.paragraph, self.quote, self.paragraph_bold_italic_anchor)
        return ("\r\n\r\n").join(elements)


class LinkFactory(factory.django.DjangoModelFactory):
    """Create content item Link for project."""

    class Meta:
        model = Link

    description = factory.Faker(
        "paragraph",
        locale="ru_RU",
        nb_sentences=5,
        variable_nb_sentences=False,
    )
    title = factory.Faker("sentence", locale="ru_RU")
    url = factory.Faker("url")


class PreambleFactory(factory.django.DjangoModelFactory):
    """Create content item Preamble for blog, news or projects."""

    class Meta:
        model = Preamble

    preamble = factory.Faker("text", locale="ru_RU")


class QuoteFactory(factory.django.DjangoModelFactory):
    """Create content item Quote for blog, news or projects."""

    class Meta:
        model = Quote

    quote = factory.Faker("text", locale="ru_RU")


class TextFactory(factory.django.DjangoModelFactory):
    """Create content item Text for blog, news or projects."""

    class Meta:
        model = Text

    text = factory.Faker(
        "paragraph",
        locale="ru_RU",
        nb_sentences=5,
        variable_nb_sentences=False,
    )


class TitleFactory(factory.django.DjangoModelFactory):
    """Create content item Title for blog, news or projects."""

    class Meta:
        model = Title

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)
