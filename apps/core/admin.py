from django.contrib import admin
from django.db import models

# from markdownx.admin import MarkdownxModelAdmin
from markdownx.widgets import AdminMarkdownxWidget

from apps.core.models import Image, MarkdownModel


class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": AdminMarkdownxWidget},
    }
    list_display = ("title",)


admin.site.register(Image)
admin.site.register(MarkdownModel, MyModelAdmin)
