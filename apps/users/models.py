from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
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
        # gr = self.groups.all().filter(name='admin')
        # print(self.groups.all().filter(name='admin'))
        return self.groups.all().filter(name="admin").exists()

    @property
    def is_editor(self):
        """
        Return True if user is editor
        """
        return self.groups.all().filter(name="editor").exists()

    def save(self, *args, **kwargs):
        print(self.groups.all())
        print(self.is_editor)
        print(self.is_admin)
        """
        Make every user is staff for access in admin panel
        """

        self.is_staff = True
        super().save(*args, **kwargs)
