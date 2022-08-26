from django.db import migrations


def rename_email_settings(apps, schema_editor):
    Setting = apps.get_model("core", "Setting")

    old_email_keys = (
        "email_on_project_page",
        "email_on_about_festival_page",
        "email_to_send_participations",
        "email_on_support_page",
    )

    Setting.objects.filter(settings_key__in=old_email_keys).delete()
    Setting.objects.filter(settings_key="email_on_volunteers_page").update(
        settings_key="volunteer_email",
        description="Email для волонтёров (страница 'О фестивале – Организаторы')",
    )
    Setting.objects.filter(settings_key="email_on_trustees_page").update(
        settings_key="trustee_email",
        description="Email для попечителей (страницы 'О фестивале – Попечители' и 'Поддержать')",
    )
    Setting.objects.filter(settings_key="email_on_acceptance_of_plays_page").update(
        settings_key="submit_play_email",
        description="Email для подачи пьес",
    )
    Setting.objects.filter(settings_key="email_on_author_page").update(
        settings_key="play_author_email",
        description="Email для авторов пьес (страницы 'Библиотека – Автор – Имя' и 'Контакты – Для авторов')",
    )
    Setting.objects.filter(settings_key="email_on_blog_page").update(
        settings_key="blog_author_email",
        description="Email для авторов блогов (страница 'Блог')",
    )
    Setting.objects.filter(settings_key="email_on_what_we_do_page").update(
        settings_key="reading_email",
        description="Email для режиссёров и актёров для читок (страницы 'О фестивале – Что мы делаем' и 'Проект – Открыть проект')"
    )
    Setting.objects.get_or_create(
        field_type="EMAIL",
        group="EMAIL",
        settings_key="press_email",
        email="press@lubimovka.ru",
        description="Email для прессы (футер – Для прессы)",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0029_auto_20220811_1627"),
    ]

    operations = [
        migrations.RunPython(
            rename_email_settings,
        ),
    ]
