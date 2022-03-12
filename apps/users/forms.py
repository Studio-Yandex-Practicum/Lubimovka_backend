from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

User = get_user_model()


class UserAdminForm(forms.ModelForm):
    def clean(self):
        groups = self.cleaned_data["groups"]

        if groups.count() > 1:
            raise ValidationError("Выбрать можно только одну группу.")


class UserAdminCreationForm(UserCreationForm, PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        help_text="Обязательное поле." " На данную почту будет выслана пользователю ссылка для смены пароля.",
        required=True,
    )
    first_name = forms.CharField(label="Имя", help_text="Обязательное поле")
    last_name = forms.CharField(label="Фамилия", help_text="Обязательное поле")

    def __init__(self, *args, **kwargs):
        super(UserAdminCreationForm, self).__init__(*args, **kwargs)
        self.fields["password1"].required = False
        self.fields["password2"].required = False

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if not user.username:
            user.username = user.email
        user.set_password(get_random_string(length=8))
        user.save()
        reset_form = PasswordResetForm({"email": user.email})
        if reset_form.is_valid():
            reset_form.save(
                subject_template_name="registration/invitation_subject.txt",
                email_template_name="registration/invitation_email.html",
            )
        return user

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
        )
        error_messages = {
            "email": {
                "unique": "Электронная почта должна быть уникальной!",
            },
        }


class GroupAdminForm(forms.ModelForm):
    """Extra field "Users" for groups."""

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
        """Add the users to the Group and remove past relations."""
        self.instance.user_set.through.objects.filter(user__in=self.cleaned_data["users"]).delete()

        self.instance.user_set.set(self.cleaned_data["users"])

    def save(self, *args, **kwargs):
        instance = super().save()
        self.save_m2m()
        return instance
