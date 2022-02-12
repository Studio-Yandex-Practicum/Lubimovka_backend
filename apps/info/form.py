from django import forms

from apps.info.models import FestivalTeam


class ManagerForm(forms.ModelForm):
    """
    Форма для дополнительного поля о данных о PR-менеджере.

    Данные пойдут в модель Setting.
    """

    data_manager = forms.CharField(
        label="Данные о PR-менеджере (в дательном падеже)",
        required=False,
        help_text="пример: Ивану Иванову",
        max_length=60,
    )


class FestivalTeamForm(ManagerForm):
    """Форма для команды-фестиваля."""

    class Meta:
        model = FestivalTeam
        fields = (
            "person",
            "team",
            "position",
            "is_pr_manager",
            "data_manager",
        )

    def __init__(self, *args, **kwargs):
        super(ManagerForm, self).__init__(*args, **kwargs)
        self.fields["data_manager"].widget.attrs["class"] = "js-person-name"

    def clean(self):
        cleaned_data = super().clean()
        is_pr_manager = cleaned_data["is_pr_manager"]
        data_manager = cleaned_data["data_manager"]

        if is_pr_manager and not data_manager:
            msg = "Дополните данные о менеджере. Укажите Имя Фамилия в дательном падеже."
            self.add_error("data_manager", msg)
