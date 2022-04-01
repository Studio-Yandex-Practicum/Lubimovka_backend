from django import forms

from apps.core.models import Setting
from apps.info.models import FestivalTeamMember


class FestTeamMemberForm(forms.ModelForm):
    """Форма для Арт дирекции фестиваля.

    Плюс дополнительное поле о данных о PR-менеджере.
    """

    def __init__(self, *args, **kwargs):
        super(FestTeamMemberForm, self).__init__(*args, **kwargs)
        if self["is_pr_director"].value():
            pr_director_name = Setting.get_setting("pr_director_name")
            self.fields["data_director"].initial = pr_director_name

    data_director = forms.CharField(
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
            "data_director",
        )

    def clean(self):
        cleaned_data = super().clean()
        is_pr_director = cleaned_data["is_pr_director"]
        data_director = cleaned_data["data_director"]

        if is_pr_director and not data_director:
            msg = "Дополните данные о PR-директоре. Укажите Имя Фамилия в дательном падеже."
            self.add_error("data_director", msg)
