import re

from django import forms


class DurationField(forms.Field):
    def to_python(self, duration):
        pattern = r"^0?\d:[0-5]\d:[0-5]\d$"
        match = re.match(pattern, duration)
        if match is None:
            return None
        return super().to_python(duration)


class PerformanceForm(forms.ModelForm):
    duration = DurationField(
        label="Продолжительность",
        help_text="Укажите продолжительность в формате ЧЧ:ММ:СС",
        error_messages={"required": "Укажите продолжительность в формате ЧЧ:ММ:СС, не более 09:59:59"},
    )
