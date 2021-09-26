from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

User = get_user_model()


class UserAdminForm(forms.ModelForm):
    def clean(self):
        groups = self.cleaned_data["groups"]

        if groups.count() > 1:
            raise ValidationError("Выбрать можно только одну группу.")


class GroupAdminForm(forms.ModelForm):
    """
    Extra field "Users" for groups
    """

    class Meta:
        model = Group
        exclude = []

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("users", False),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["users"].initial = self.instance.user_set.all()

    def save_m2m(self):
        """
        Add the users to the Group and remove past relations.
        """

        self.instance.user_set.through.objects.filter(
            user__in=self.cleaned_data["users"]
        ).delete()

        self.instance.user_set.set(self.cleaned_data["users"])

    def save(self, *args, **kwargs):
        instance = super().save()
        self.save_m2m()
        return instance
