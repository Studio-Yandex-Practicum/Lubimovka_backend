from django.contrib import admin

from apps.articles.models import BlogItem, BlogItemContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin
from apps.core.mixins import InlineReadOnlyMixin, StatusButtonMixin
from apps.library.utilities import CustomAutocompleteSelect


class BlogPersonInline(InlineReadOnlyMixin, admin.TabularInline):
    model = BlogItem.roles.through
    autocomplete_fields = ("person",)
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "person":
            db = kwargs.get("using")
            kwargs["widget"] = CustomAutocompleteSelect(
                db_field, self.admin_site, using=db, placeholder="Выберите человека"
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class BlogItemContentInline(InlineReadOnlyMixin, BaseContentInline):
    model = BlogItemContent
    content_type_model = (
        "imagesblock",
        "personsblock",
        "playsblock",
        "preamble",
        "quote",
        "text",
        "title",
    )


class BlogItemAdmin(StatusButtonMixin, BaseContentPageAdmin):
    list_display = (
        "title",
        "description",
        "pub_date",
        "image_preview_list_page",
        "status",
    )
    readonly_fields = (
        "status",
        "image_preview_change_page",
    )
    inlines = (
        BlogPersonInline,
        BlogItemContentInline,
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "status",
                    "title",
                    (
                        "author_url_title",
                        "author_url",
                    ),
                    "pub_date",
                    "description",
                    (
                        "image_preview_change_page",
                        "image",
                    ),
                )
            },
        ),
    )
    other_readonly_fields = (
        "status",
        "title",
        "author_url_title",
        "author_url",
        "pub_date",
        "description",
        "image_preview_change_page",
        "image",
    )


admin.site.register(BlogItem, BlogItemAdmin)
