from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin

from apps.core.mixins import AdminImagePreview

from ..models import ContentImagesBlockItem


class ContentBlockItemInline(SortableInlineAdminMixin, admin.TabularInline):
    min_num = 1
    extra = 0


class ContentImagesBlockItemInline(AdminImagePreview, ContentBlockItemInline):
    readonly_fields = ("image_preview_change_page",)
    model = ContentImagesBlockItem
    max_num = 8
