from django.contrib import admin

from .models import Partners


class PartnersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'type',
        'url',
        #'image',

    )
    empty_value_display = "-пусто-"

admin.site.register(Partners, PartnersAdmin)