from django import forms
from django_select2 import forms as s2forms

from apps.library.models import Performance, Play, Reading


class OtherLinkForm(forms.ModelForm):
    """Reduce field link in OtherLinkInline."""

    class Meta:
        widgets = {
            "link": forms.TextInput(attrs={"size": 30}),
        }


class PlayAdminForm(forms.ModelForm):
    """Add autocomplete fields."""

    class Meta:
        model = Play
        fields = "__all__"
        widgets = {
            "program": s2forms.Select2Widget(
                attrs={
                    "data-placeholder": "Выберите программу",
                    "data-allow-clear": "true",
                }
            ),
            "festival": s2forms.Select2Widget(
                attrs={
                    "data-placeholder": "Выберите фестиваль",
                    "data-allow-clear": "true",
                }
            ),
        }


class PerformanceAdminForm(forms.ModelForm):
    """Add autocomplete fields."""

    class Meta:
        model = Performance
        fields = "__all__"
        widgets = {
            "play": s2forms.Select2Widget(
                attrs={
                    "data-placeholder": "Выберите пьесу",
                    "data-allow-clear": "true",
                }
            ),
            "age_limit": s2forms.Select2Widget(
                attrs={
                    "data-placeholder": "Выберите возраст",
                    "data-allow-clear": "true",
                }
            ),
            "project": s2forms.Select2Widget(
                attrs={
                    "data-placeholder": "Выберите проект",
                    "data-allow-clear": "true",
                }
            ),
        }


class ReadingAdminForm(forms.ModelForm):
    """Add autocomplete fields."""

    class Meta:
        model = Reading
        fields = "__all__"
        widgets = {
            "play": s2forms.Select2Widget(
                attrs={
                    "data-placeholder": "Выберите пьесу",
                    "data-allow-clear": "true",
                }
            ),
            "project": s2forms.Select2Widget(
                attrs={
                    "data-placeholder": "Выберите проект",
                    "data-allow-clear": "true",
                }
            ),
        }
