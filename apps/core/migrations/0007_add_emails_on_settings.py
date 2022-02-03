from django.db import migrations


def add_email_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.get_or_create(
        field_type="EMAIL",
        group="EMAIL",
        settings_key="email_for_press",
        email="press@gmail.com",
        description="почта для вопросов по PR",
    )
    Setting.objects.get_or_create(
        field_type="EMAIL",
        group="EMAIL",
        settings_key="email_on_project_page",
        email="project@gmail.com",
        description="почта чтобы присоединиться как режиссер",
    )
    Setting.objects.get_or_create(
        field_type="EMAIL",
        group="EMAIL",
        settings_key="email_on_organizers_page",
        email="organizers@gmail.com",
        description="почта для заявок от волонтеров",
    )
    Setting.objects.get_or_create(
        field_type="EMAIL",
        group="EMAIL",
        settings_key="email_on_trustees_page",
        email="trustees@gmail.com",
        description="почта чтобы стать попечителем",
    )
    Setting.objects.get_or_create(
        field_type="EMAIL",
        group="EMAIL",
        settings_key="email_on_about_festival_page",
        email="festival@gmail.com",
        description="почта чтобы стать режиссером одной из читок",
    )
    Setting.objects.get_or_create(
        field_type="EMAIL",
        group="EMAIL",
        settings_key="email_on_acceptance_of_plays_page",
        email="plays@gmail.com",
        description="почта для заявок на участие",
    )
    Setting.objects.get_or_create(
        field_type="EMAIL",
        group="EMAIL",
        settings_key="email_on_author_page",
        email="author@gmail.com",
        description="почта для внесений изменений об авторе",
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
