from django.contrib import admin
from django.db import models
from django_select2 import forms as s2forms

from apps.library.models import PerformanceReview


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = (
        "reviewer_name",
        "performance",
        "pub_date",
    )
    list_filter = (
        "reviewer_name",
        "performance__name",
        "pub_date",
    )
    search_fields = (
        "reviewer_name",
        "performance__name",
        "pub_date",
    )
    readonly_fields = ("pub_date",)
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
