from django import forms

from apps.library.models import Play, ProgramType


class MainPlayForm(forms.ModelForm):
    class Meta:
        model = Play
        exclude = ("link",)
        fields = ("name", "city", "year", "url_download", "url_reading", "program", "festival", "published")


class OtherPlayForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OtherPlayForm, self).__init__(*args, **kwargs)
        self.fields["program"].initial = ProgramType.objects.get(slug="other_plays")

    class Meta:
        model = Play
        fields = ("name", "program", "link")
