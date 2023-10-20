from filer.admin import FileAdmin, ImageAdmin
from filer.admin.fileadmin import FileAdminChangeFrom
from filer.admin.imageadmin import ImageAdminForm


class ShortImageAdminForm(ImageAdminForm):
    class Media:
        css = {"all": ("custom_filer.css",)}


class ShortFileAdminForm(FileAdminChangeFrom):
    class Media:
        css = {"all": ("custom_filer.css",)}


class NonEditableImageAdmin(ImageAdmin):
    form = ShortImageAdminForm


class NonEditableFileAdmin(FileAdmin):
    form = ShortImageAdminForm
