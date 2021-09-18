from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        EDITOR = "Редактор", "Редактор"
        ADMIN = "Администратор", "Администратор"

    role = models.CharField(
        max_length=13,
        choices=Role.choices,
        default=Role.EDITOR,
        verbose_name="Роль",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        """
        Return True if user is admin
        """
        return self.role == self.Role.ADMIN

    @property
    def is_editor(self):
        """
        Return True if user is editor
        """
        return self.role == self.Role.EDITOR

    def save(self, *args, **kwargs):
        """
        Make every user is staff for access in admin panel
        """
        self.is_staff = True
        super().save(*args, **kwargs)
