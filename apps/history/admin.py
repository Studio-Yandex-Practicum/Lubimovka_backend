from django.contrib import admin

from apps.history.models import History, HistoryQuestion


class HistoryAdmin(admin.ModelAdmin):
    pass


class HistoryQuestionAdmin(admin.ModelAdmin):
    pass


admin.site.register(History, HistoryAdmin)
admin.site.register(HistoryQuestion, HistoryQuestionAdmin)
