from typing import Union

from apps.core.models import Person, Setting


def info_settings_get() -> dict[str, Union[str, bool, dict[str, str]]]:
    """Return settings (mostly related to emails) dictionary."""
    settings_keys = (
        "email_on_project_page",
        "email_on_what_we_do_page",
        "email_on_trustees_page",
        "email_on_about_festival_page",
        "email_on_acceptance_of_plays_page",
        "email_on_author_page",
        "email_on_volunteers_page",
        "email_on_blog_page",
        "email_on_support_page",
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
