from django import forms

from apps.library.models import ProgramType


class PlayForm(forms.ModelForm):
    program = forms.ModelChoiceField(queryset=ProgramType.objects.all(), to_field_name="slug", label="Программа")
