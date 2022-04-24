from django import forms

from apps.core.models import Setting
from apps.info.models import FestivalTeamMember


class FestTeamMemberForm(forms.ModelForm):
    """Форма для Команды фестиваля.

    Плюс дополнительное поле о данных о PR-директоре.
    """

    def __init__(self, *args, **kwargs):
        super(FestTeamMemberForm, self).__init__(*args, **kwargs)
        if self["is_pr_director"].value():
            pr_director_dative_name = Setting.get_setting("pr_director_dative_name")
            self.fields["pr_director_dative_name"].initial = pr_director_dative_name

    pr_director_dative_name = forms.CharField(
        label="Данные о PR-директоре (в дательном падеже)",
        required=False,
        help_text="пример: Ивану Иванову",
        max_length=60,
    )

    class Meta:
        model = FestivalTeamMember
        exclude = ("team",)
        fields = (
            "person",
            "position",
            "is_pr_director",
            "pr_director_dative_name",
        )

    def clean(self):
        cleaned_data = super().clean()
        is_pr_director = cleaned_data["is_pr_director"]
        pr_director_dative_name = cleaned_data["pr_director_dative_name"]

        if is_pr_director and not pr_director_dative_name:
            msg = "Дополните данные о PR-директоре. Укажите Имя Фамилия в дательном падеже."
            self.add_error("pr_director_dative_name", msg)
