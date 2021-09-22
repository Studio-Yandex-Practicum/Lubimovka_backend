from django.contrib import admin

from .models import Partner, Question


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


admin.site.register(Partner, PartnerAdmin)
admin.site.register(Question, QuestionAdmin)
