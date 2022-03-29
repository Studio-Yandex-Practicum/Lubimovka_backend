from django.contrib import admin
from django.db import models
from django_select2 import forms as s2forms

from apps.library.models import PerformanceMediaReview


@admin.register(PerformanceMediaReview)
class PerformanceMediaReviewAdmin(admin.ModelAdmin):
    list_display = (
        "media_name",
        "performance",
        "pub_date",
    )
    list_filter = (
        "media_name",
        "performance__name",
        "pub_date",
    )
    search_fields = (
        "media_name",
        "performance__name",
        "pub_date",
    )
    readonly_fields = ("pub_date",)
    autocomplete_fields = ("performance",)
    formfield_overrides = {
        models.ForeignKey: {
            "widget": s2forms.Select2Widget(
                attrs={
                    "data-placeholder": "Выберите спектакль",
                    "data-allow-clear": "true",
                }
            )
        }
    }
