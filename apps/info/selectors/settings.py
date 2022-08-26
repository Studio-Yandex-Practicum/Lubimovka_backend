from typing import Union

from apps.core.models import Person, Setting


def info_settings_get() -> dict[str, Union[str, bool, dict[str, str]]]:
    """Return settings (mostly related to emails) dictionary."""
    settings_keys = (
        "play_author_email",
        "blog_author_email",
        "reading_email",
        "volunteer_email",
        "trustee_email",
        "press_email",
        "submit_play_email",
        "photo_gallery_facebook",
        "pr_director_name",
        "url_to_privacy_policy",
        "plays_reception_is_open",
    )
    info_settings_data = Setting.get_settings(settings_keys)

    pr_director = Person.objects.filter(festivalteammember__is_pr_director=True).first()
    pr_director_email = pr_director.email if pr_director else None
    pr_director_photo_link = pr_director.image if pr_director else None
    photo_gallery_facebook = info_settings_data.pop("photo_gallery_facebook")
    pr_director_name = info_settings_data.pop("pr_director_name")
    for_press = {
        "pr_director": {
            "pr_director_name": pr_director_name,
            "pr_director_email": pr_director_email,
            "pr_director_photo_link": pr_director_photo_link,
        },
        "photo_gallery_facebook_link": photo_gallery_facebook,
    }

    info_settings_data["for_press"] = for_press

    return info_settings_data
