from django.contrib import admin
from django.db import models
from markdownx.widgets import AdminMarkdownxWidget

from apps.static_pages.models import StaticPagesModel


class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": AdminMarkdownxWidget},
    }
    list_display = ("page_type",)


admin.site.register(StaticPagesModel, MyModelAdmin)
