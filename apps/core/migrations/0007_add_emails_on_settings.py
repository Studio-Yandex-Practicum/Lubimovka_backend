from django.db import migrations


def add_email_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.get_or_create(
        field_type="EMAIL",
        group="EMAIL",
        settings_key="email_on_project_page",
        email="project@gmail.com",
        description="Почта, чтобы присоединиться как режиссер",
    )
    Setting.objects.get_or_create(
        field_type="EMAIL",
        group="EMAIL",
        settings_key="email_on_what_we_do_page",
        email="organizers@gmail.com",
        description="Почта, чтобы присоединиться как режиссёр на странице «Что мы делаем»",
    )
    Setting.objects.get_or_create(
        field_type="EMAIL",
        group="EMAIL",
        settings_key="email_on_trustees_page",
        email="trustees@gmail.com",
        description="Почта, чтобы стать попечителем",
    )
    Setting.objects.get_or_create(
        field_type="EMAIL",
        group="EMAIL",
        settings_key="email_on_about_festival_page",
        email="festival@gmail.com",
        description="Почта для сотрудничества режиссёров и актёров",
    )
    Setting.objects.get_or_create(
        field_type="EMAIL",
        group="EMAIL",
        settings_key="email_on_acceptance_of_plays_page",
        email="plays@gmail.com",
        description="Почта для заявок на участие",
    )
    Setting.objects.get_or_create(
        field_type="EMAIL",
        group="EMAIL",
        settings_key="email_on_author_page",
        email="author@gmail.com",
        description="Почта для внесений изменений об авторе",
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_facebook_photo_gallery_link'),
    ]

    operations = [
        migrations.RunPython(
            add_email_settings,
        ),
    ]
