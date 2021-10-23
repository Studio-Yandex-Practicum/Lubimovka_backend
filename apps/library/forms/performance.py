from django import forms
from django.core.exceptions import ValidationError

from apps.library.models import Performance


class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = "__all__"

    def clean(self):
        images_in_block = self.cleaned_data.get("images_in_block")
        if images_in_block.count() > 8:
            raise ValidationError({"images_in_block": "Too many images!"})
        return self.cleaned_data
