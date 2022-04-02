from django import forms

from apps.library.models import ProgramType


class ProgramChoiceField(forms.ModelChoiceField):
    def prepare_value(self, value):
        if hasattr(value, "_meta"):
            if self.to_field_name:
                return value.serializable_value(self.to_field_name)
            else:
                return value.pk
        if self.to_field_name:
            #  this part needs to show correctly alreade selected and saved value
            selected_value = [_ for _ in self.queryset if _.pk == value]
            if selected_value:
                return getattr(selected_value[0], self.to_field_name)
        return super().prepare_value(value)


class PlayForm(forms.ModelForm):
    program = ProgramChoiceField(
        queryset=ProgramType.objects.all(),
        to_field_name="slug",
        label="Программа",
        empty_label=None,
    )
