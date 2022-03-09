from django import forms

from apps.core.utils import slugify


class AuthorForm(forms.ModelForm):
    def clean(self):
        person = self.cleaned_data.get("person")
        full_name = person.first_name + "_" + person.last_name
        slug = slugify(full_name)
        self.fields["slug"].error_messages = {
            "unique": f"Tранслит '{slug}' уже используется, необходимо ввести оригинальный вручную",
        }
        return super().clean()
