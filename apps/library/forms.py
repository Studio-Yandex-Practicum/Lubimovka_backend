from django import forms

from apps.library.models import Play


class OtherLinkForm(forms.ModelForm):
    """Reduce field link in OtherLinkInline."""

    class Meta:
        widgets = {
            "link": forms.TextInput(attrs={"size": 30}),
        }


class PlayInlineForm(forms.ModelForm):
    """Used to optimize database queries in AuthorPlay inlines."""

    play_choices = [("", "-----")]
    for item in Play.objects.filter(other_play=False).values("id", "name", "published"):
        if item["published"]:
            play_choices.append((item["id"], item["name"]))
        else:
            play_choices.append((item["id"], f"{item['name']} - НЕ ОПУБЛИКОВАНА"))
    play = forms.ChoiceField(required=True, choices=play_choices)


class OtherPlayInlineForm(forms.ModelForm):
    """Used to optimize database queries in AuthorPlay inlines."""

    play_choices = [("", "-----")]
    for item in Play.objects.filter(other_play=True).values("id", "name", "published"):
        if item["published"]:
            play_choices.append((item["id"], item["name"]))
        else:
            play_choices.append((item["id"], f"{item['name']} - НЕ ОПУБЛИКОВАНА"))
    play = forms.ChoiceField(required=True, choices=play_choices)
