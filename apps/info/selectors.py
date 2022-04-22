from typing import Any

from apps.core.models import Person, Setting


def info_settings_get() -> dict[str, Any]:
    """Return feedback settings (mostly related to emails) dictionary."""
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
        "plays_reception_is_open",
    )
    feedback_settings_data = Setting.get_settings(settings_keys)

    pr_director = Person.objects.filter(festivalteammember__is_pr_director=True).first()
    for_press = {
        "pr_director": {
            "pr_director_name": feedback_settings_data["pr_director_name"],
            "pr_director_email": pr_director.email,
            "pr_director_photo_link": pr_director.image,
        },
        "photo_gallery_facebook_link": feedback_settings_data["photo_gallery_facebook"],
    }
    feedback_settings_data["for_press"] = for_press
    [feedback_settings_data.pop(key) for key in ["pr_director_name", "photo_gallery_facebook"]]

    return feedback_settings_data
