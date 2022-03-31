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
            pr_director_name = Setting.objects.filter(settings_key="pr_director_name").first()
            self.fields["data_manager"].initial = pr_director_name.text

    data_manager = forms.CharField(
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
            "data_manager",
        )

    def clean(self):
        cleaned_data = super().clean()
        is_pr_director = cleaned_data["is_pr_director"]
        data_manager = cleaned_data["data_manager"]

        if is_pr_director and not data_manager:
            msg = "Дополните данные о PR-директоре. Укажите Имя Фамилия в дательном падеже."
            self.add_error("data_manager", msg)
