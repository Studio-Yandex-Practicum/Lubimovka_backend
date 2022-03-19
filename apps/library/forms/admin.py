from django import forms


class OtherLinkForm(forms.ModelForm):
    class Meta:
        widgets = {
            "link": forms.TextInput(attrs={"size": 30}),
        }
