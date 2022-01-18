from django.contrib import admin

from apps.content_pages.models import Image, Link, Preamble, Quote, Text, Title, Video
from apps.core.mixins import AdminImagePreview, ModelAdminToHide


@admin.register(Image)
class ImageAdmin(AdminImagePreview, ModelAdminToHide):
    list_display = (
        "id",
        "image_preview_list_page",
    )
    readonly_fields = ("image_preview_change_page",)


admin.site.register(Preamble, ModelAdminToHide)
admin.site.register(Link, ModelAdminToHide)
admin.site.register(Quote, ModelAdminToHide)
admin.site.register(Text, ModelAdminToHide)
admin.site.register(Title, ModelAdminToHide)
admin.site.register(Video, ModelAdminToHide)
