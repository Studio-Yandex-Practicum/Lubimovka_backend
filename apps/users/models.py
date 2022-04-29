from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.first_name = user.username
        user.save()
        return user


class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True, verbose_name="Имя пользователя", unique=True)
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Электронная почта")

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username} ({self.groups.first() if self.groups.first() else '-'})"

    @property
    def is_admin(self):
        """Return True if user is admin."""
        return self.groups.filter(name="admin").exists()

    @property
    def is_editor(self):
        """Return True if user is editor."""
        return self.groups.filter(name="editor").exists()

    def save(self, *args, **kwargs):
        """Set "is_staff" for each user."""
        if self._state.adding:
            self.is_staff = True
        super().save(*args, **kwargs)


class ProxyGroup(Group):
    """Ordinary django's Group. The class is required to register model in `users` app."""

    class Meta:
        proxy = True
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
