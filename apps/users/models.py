from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
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
        self.is_staff = True
        super().save(*args, **kwargs)


class ProxyUser(User):
    pass

    class Meta:
        app_label = "auth"
        proxy = True
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
