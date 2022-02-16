from django import forms

from apps.info.models import FestivalTeam


class FestivalTeamForm(forms.ModelForm):
    """Форма для команды-фестиваля.

    Плюс дополнительное поле о данных о PR-менеджере.
    """

    data_manager = forms.CharField(
        label="Данные о PR-менеджере (в дательном падеже)",
        required=False,
        help_text="пример: Ивану Иванову",
        max_length=60,
    )

    class Meta:
        model = FestivalTeam
        fields = (
            "person",
            "team",
            "position",
            "is_pr_manager",
            "data_manager",
        )

    def clean(self):
        cleaned_data = super().clean()
        is_pr_manager = cleaned_data["is_pr_manager"]
        data_manager = cleaned_data["data_manager"]

        if is_pr_manager and not data_manager:
            msg = "Дополните данные о менеджере. Укажите Имя Фамилия в дательном падеже."
            self.add_error("data_manager", msg)
