from django import forms


class OtherLinkForm(forms.ModelForm):
    """Reduce field link in OtherLinkInline."""

    class Meta:
        widgets = {
            "link": forms.TextInput(attrs={"size": 30}),
        }
