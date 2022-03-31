from django import forms
from django.core.exceptions import ValidationError

from apps.library.models import ProgramType


class PlayForm(forms.ModelForm):
    program = forms.ModelChoiceField(queryset=ProgramType.objects.all(), to_field_name="slug", label="Программа")

    def clean(self):
        cleaned_data = super().clean()
        program = cleaned_data.get("program")
        festival = cleaned_data.get("festival")
        if program and not festival:
            if program.slug != "other_plays":
                raise ValidationError("У пьесы Любимовки должен быть фестиваль")
