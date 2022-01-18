from django.db import migrations


def add_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.create(
        field_type="TEXT",
        group="AFISHA",
        settings_key="afisha_title_festival",
        text="Афиша фестиваля",
        description="Заголовок афиши во время фестиваля",
    )
    Setting.objects.create(
        field_type="TEXT",
        group="AFISHA",
        settings_key="afisha_title_regular",
        text="Афиша событий",
        description="Заголовок афиши регулярный",
    )
    Setting.objects.create(
        field_type="TEXT",
        group="AFISHA",
        settings_key="afisha_description_festival",
        text="На все читки и мастер-классы фестиваля вход свободный по предварительной регистрации.",
        description="Описание под заголовком во время фестиваля",
    )
    Setting.objects.create(
        field_type="TEXT",
        group="AFISHA",
        settings_key="afisha_description_regular",
        text="На все читки и мастер-классы фестиваля вход свободный по предварительной регистрации.",
        description="Описание под заголовком регулярное",
    )
    Setting.objects.create(
        field_type="TEXT",
        group="AFISHA",
        settings_key="afisha_info_festival_text",
        text="Регистрация на каждое мероприятие открывается в 12:00 предыдущего дня.",
        description="Информация о регистрации на событие фестиваля",
    )
    Setting.objects.create(
        field_type="TEXT",
        group="AFISHA",
        settings_key="afisha_asterisk_text",
        text="После каждой читки будет проходить обсуждение с участием аудитории, автора и театральных профессионалов.",
        description="Текст со звёздочкой возле заголовка",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0026_delete_old_afisha_settings"),
    ]

    operations = [migrations.RunPython(add_settings)]
