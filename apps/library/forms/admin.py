from django import forms

from apps.core.utils import slugify


class AuthorForm(forms.ModelForm):
    def clean(self):
        slug = self.cleaned_data.get("slug")
        person = self.cleaned_data.get("person")
        if not slug:
            slug = slugify(person.last_name)
        self.fields["slug"].error_messages = {
            "unique": f"Tранслит '{slug}' уже используется, необходимо ввести оригинальный вручную",
        }
        return super().clean()


class OtherLinkForm(forms.ModelForm):
    class Meta:
        widgets = {
            "link": forms.TextInput(attrs={"size": 30}),
        }
