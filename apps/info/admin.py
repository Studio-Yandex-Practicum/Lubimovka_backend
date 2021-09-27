from django.contrib import admin

from .models import Partner, Place, Question


class PartnerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "type",
        "url",
        # 'image',
    )
    empty_value_display = "-пусто-"


class QuestionAdmin(admin.ModelAdmin):
    pass


class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "city",
        "address",
    )

    list_filter = ("city",)
    search_fields = ("name", "address")


admin.site.register(Partner, PartnerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Place, PlaceAdmin)
