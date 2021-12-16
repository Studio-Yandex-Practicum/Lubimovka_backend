from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class ProxyUser(User):
    pass

    class Meta:
        app_label = "auth"
        proxy = True
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
