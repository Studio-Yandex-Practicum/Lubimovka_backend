from django import forms
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.core.models import Setting
from apps.core.services.send_email import send_email

User = get_user_model()


class UserAdminForm(UserChangeForm):
    def clean(self):
        groups = self.cleaned_data["groups"]

        if groups.count() > 1:
            raise ValidationError("Выбрать можно только одну группу.")


class UserAdminPasswordResetForm(PasswordResetForm):
    def send_email_to_user(self, from_email, template_id, domain):
        email = self.cleaned_data["email"]
        email_field_name = User.get_email_field_name()

        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            context = {
                "full_name": user.get_full_name(),
                "username": user.get_username(),
                "email": user_email,
                "domain": domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            }
            send_email(
                from_email=from_email,
                to_emails=(user_email,),
                template_id=template_id,
                context=context,
            )


class UserAdminCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        help_text=(
            "Обязательное поле. На данную почту пользователю будет выслана ссылка для смены и восстановления пароля."
        ),
        required=True,
    )
    first_name = forms.CharField(label="Имя", help_text="Обязательное поле")
    last_name = forms.CharField(label="Фамилия", help_text="Обязательное поле")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].required = False
        self.fields["password2"].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if not user.username:
            user.username = user.email
        user.set_password(get_random_string(length=8))
        user.save()
        reset_form = UserAdminPasswordResetForm({"email": user.email})
        if reset_form.is_valid():
            reset_form.send_email_to_user(
                from_email=Setting.get_setting("email_send_from"),
                template_id=settings.MAILJET_TEMPLATE_ID_CHANGE_PASSWORD_USER,
                domain=self.domain,
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
