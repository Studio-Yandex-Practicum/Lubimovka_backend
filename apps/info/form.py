from django import forms

from apps.core.models import Setting
from apps.info.models import FestivalTeamMember, InfoLink


class FestTeamMemberForm(forms.ModelForm):
    """Форма для Команды фестиваля.

    Плюс дополнительное поле о данных о PR-директоре.
    """

    def __init__(self, *args, **kwargs):
        super(FestTeamMemberForm, self).__init__(*args, **kwargs)
        if self["is_pr_director"].value():
            pr_director_name = Setting.get_setting("pr_director_name")
            self.fields["pr_director_name"].initial = pr_director_name

    pr_director_name = forms.CharField(
        label="Данные о PR-директоре (в дательном падеже)",
        required=False,
        help_text="пример: Ивану Иванову",
        max_length=60,
    )
    team = forms.CharField(widget=forms.HiddenInput(), initial="fest")

    class Meta:
        model = FestivalTeamMember
        fields = (
            "person",
            "position",
            "is_pr_director",
            "pr_director_name",
            "team",
        )

    def clean(self):
        cleaned_data = super().clean()
        is_pr_director = cleaned_data["is_pr_director"]
        pr_director_name = cleaned_data["pr_director_name"]

        if is_pr_director and not pr_director_name:
            msg = "Дополните данные о PR-директоре. Укажите Имя Фамилия в дательном падеже."
            self.add_error("pr_director_name", msg)


class ArtTeamMemberForm(forms.ModelForm):
    """Форма для Арт-дирекции фестиваля."""

    team = forms.CharField(widget=forms.HiddenInput(), initial="art")

    class Meta:
        model = FestivalTeamMember
        fields = (
            "person",
            "position",
            "team",
        )


class AdditionalLinkForm(forms.ModelForm):
    """Set type to InfoLink according to inline."""

    class Meta:
        model = InfoLink
        fields = (
            "title",
            "link",
        )

    def save(self, commit=True):
        new_link = super().save(commit=False)
        new_link.type = InfoLink.LinkType.ADDITIONAL_LINKS
        new_link.save()
        return new_link


class PlayLinkForm(forms.ModelForm):
    """Set type to InfoLink according to inline."""

    class Meta:
        model = InfoLink
        fields = (
            "title",
            "link",
        )

    def save(self, commit=True):
        new_link = super().save(commit=False)
        new_link.type = InfoLink.LinkType.PLAYS_LINKS
        new_link.save()
        return new_link


class FestivalForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, label="Описание фестиваля", max_length=200)
