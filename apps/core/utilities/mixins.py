from django.utils.html import format_html


class AdminImagePreview:

    """
    Mixin makes preview for uploaded images
    Add parameters in admin class
        list_display = ("image_preview_list_page",)
        readonly_fields = ("image_preview_change_page",)
    """

    def image_preview_change_page(self, obj):
        return format_html(
            '<img src="{}" width="600" height="300" />'.format(obj.image.url)
        )

    image_preview_change_page.short_description = "Превью"

    def image_preview_list_page(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="50" />'.format(
                    obj.image.url
                )
            )
        pass

    image_preview_list_page.short_description = "Превью"
