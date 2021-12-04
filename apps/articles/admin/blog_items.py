from django.contrib import admin

from apps.articles.models import BlogItem, BlogItemContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin
from apps.core.models import Role


class BlogPersonInline(admin.TabularInline):
    model = BlogItem.roles.through
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "role":
            kwargs["queryset"] = Role.objects.filter(
                type_roles__role_type="blog_persons_roles"
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class BlogItemContentInline(BaseContentInline):
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


class BlogItemAdmin(BaseContentPageAdmin):
    inlines = (
        BlogPersonInline,
        BlogItemContentInline,
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
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
                    "is_draft",
                )
            },
        ),
    )


admin.site.register(BlogItem, BlogItemAdmin)
