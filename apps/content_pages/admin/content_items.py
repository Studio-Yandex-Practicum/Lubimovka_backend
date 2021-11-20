from django.contrib import admin

from apps.content_pages.models import Image, Link, Quote, Text, Title, Video
from apps.core.utilities.mixins import AdminImagePreview


class ImageAdmin(AdminImagePreview, admin.ModelAdmin):
    list_display = (
        "id",
        "image_preview_list_page",
    )
    readonly_fields = ("image_preview_change_page",)


admin.site.register(Image, ImageAdmin)
admin.site.register(Link)
admin.site.register(Quote)
admin.site.register(Text)
admin.site.register(Title)
admin.site.register(Video)
