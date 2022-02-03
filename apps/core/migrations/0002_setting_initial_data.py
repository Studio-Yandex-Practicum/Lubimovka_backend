import django.contrib.auth.validators
from django.db import migrations
import django.utils.timezone


def set_default_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.bulk_create(
        [
            Group(name="admin"),
            Group(name="editor"),
        ]
    )

def create_roles(apps, schema_editor):
    Role = apps.get_model("core", "Role")
    roles = [
        {
            "name": "Актёр",
            "name_plural": "Актёры",
            "slug": "actor",
        },
        {
            "name": "Адаптация текста",
            "name_plural": "Адаптация текста",
            "slug": "text_adaptation",
        },
        {
            "name": "Драматург",
            "name_plural": "Драматурги",
            "slug": "dramatist",
        },
        {
            "name": "Режиссёр",
            "name_plural": "Режиссёры",
            "slug": "director",
        },
        {
            "name": "Переводчик",
            "name_plural": "Переводчики",
            "slug": "translator",
        },
        {
            "name": "Ведущий",
            "name_plural": "Ведущие",
            "slug": "host",
        },
        {
            "name": "Текст",
            "name_plural": "Текст",
            "slug": "text",
        },
        {
            "name": "Иллюстрации",
            "name_plural": "Иллюстрации",
            "slug": "illustrations",
        },
        {
            "name": "Фото",
            "name_plural": "Фото",
            "slug": "photo",
        },
    ]
    for role in roles:
        role_obj, _ = Role.objects.get_or_create(**role)
        role_obj.save()

def create_role_types(apps, schema_editor):
    RoleType = apps.get_model("core", "RoleType")
    role_types = [
        {
            "role_type": "blog_persons_role",
        },
        {
            "role_type": "performanse_role",
        },
        {
            "role_type": "play_role",
        },
        {
            "role_type": "master_class_role",
        },
        {
            "role_type": "reading_role",
        },
    ]
    for type in role_types:
        type_obj, _ = RoleType.objects.get_or_create(**type)
        type_obj.save()

def add_types_to_roles(apps, schema_editor):
    Role = apps.get_model("core", "Role")
    RoleType = apps.get_model("core", "RoleType")
    roles = [
        {
            "name": "Актёр",
            "slug": "actor",
            "types": "performanse_role",
        },
        {
            "name": "Адаптация текста",
            "slug": "text_adaptation",
            "types": "blog_persons_role",
        },
        {
            "name": "Драматург",
            "slug": "dramatist",
            "types": "play_role",
        },
        {
            "name": "Драматург",
            "slug": "dramatist",
            "types": "performanse_role",
        },
        {
            "name": "Драматург",
            "slug": "dramatist",
            "types": "reading_role",
        },
        {
            "name": "Режиссёр",
            "slug": "director",
            "types": "performanse_role",
        },
        {
            "name": "Режиссёр",
            "slug": "director",
            "types": "reading_role",
        },
        {
            "name": "Переводчик",
            "slug": "translator",
            "types": "blog_persons_role",
        },
        {
            "name": "Ведущий",
            "slug": "host",
            "types": "play_role",
        },
        {
            "name": "Ведущий",
            "slug": "host",
            "types": "master_class_role",
        },
        {
            "name": "Текст",
            "slug": "text",
            "types": "blog_persons_role",
        },
        {
            "name": "Иллюстрации",
            "slug": "illustrations",
            "types": "blog_persons_role",
        },
        {
            "name": "Фото",
            "slug": "photo",
            "types": "blog_persons_role",
        },
    ]
    for role in roles:
        role_obj = Role.objects.get(name=role["name"])
        type_of_role = RoleType.objects.get(role_type=role["types"])
        role_obj.types.add(type_of_role)
        role_obj.save()

def add_email_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.create(
        field_type="TEXT",
        group="EMAIL",
        settings_key="email_question_template_id",
        text="3420599",
        description="Id шаблона письма с вопросом",
    )
    Setting.objects.create(
        field_type="TEXT",
        group="EMAIL",
        settings_key="email_send_from",
        text="questions@lyubimovka.ru",
        description="Почта для отправки вопроса",
    )
    Setting.objects.create(
        field_type="TEXT",
        group="EMAIL",
        settings_key="email_send_to",
        text="admin@lyubimovka.ru",
        description="Почта для приёма вопроса",
    )
    Setting.objects.create(
        field_type="TEXT",
        group="EMAIL",
        settings_key="email_subject_for_question",
        text="Вопрос Любимовке",
        description="Тема письма для вопроса",
    )

def add_afisha_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

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

def add_first_screen_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.create(
        field_type="IMAGE",
        group="FIRST_SCREEN",
        settings_key="main_first_screen_image",
        image="core/2021-09-30_14.37.56.jpg",
        description="Изображение для первой страницы",
    )
    Setting.objects.create(
        field_type="BOOLEAN",
        group="FIRST_SCREEN",
        settings_key="main_add_first_screen",
        boolean=True,
        description="Отображение первой страницы",
    )
    Setting.objects.create(
        field_type="TEXT",
        group="FIRST_SCREEN",
        settings_key="main_first_screen_title",
        text="Открыт прием пьес на фестиваль 2021 года",
        description="Заголовок для первой страницы",
    )
    Setting.objects.create(
        field_type="TEXT",
        group="FIRST_SCREEN",
        settings_key="main_first_screen_url_title",
        text="Заголовок для ссылки для первой страницы",
        description="Заголовок для первой страницы",
    )
    Setting.objects.create(
        field_type="URL",
        group="FIRST_SCREEN",
        settings_key="main_first_screen_url",
        url="https://lubimovks.url.ru",
        description="Ссылка для первой страницы страницы",
    )

def add_general_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.create(
        field_type="BOOLEAN",
        group="GENERAL",
        settings_key="festival_status",
        boolean=True,
        description="Статус фестиваля",
    )
    Setting.objects.create(
        field_type="TEXT",
        group="GENERAL",
        settings_key="site_color",
        text="green",
        description="Цвет сайта",
    )
    Setting.objects.create(
        field_type="BOOLEAN",
        group="GENERAL",
        settings_key="form_to_submit_a_play",
        boolean=True,
        description="Форма для отправки пьесы",
    )
    Setting.objects.create(
        field_type="URL",
        group="GENERAL",
        settings_key="url_to_privacy_policy",
        url="privacy-policy",
        description="Ссылка на обработку персональных данных",
    )

    Setting.objects.create(
        field_type="URL",
        group="GENERAL",
        settings_key="photo_gallery_facebook",
        url="https://www.facebook.com/festival.lubimovka/photos",
        description="Ссылка на фотоальбомы в Facebook на странице для прессы",
    )

def add_main_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.create(
        field_type="BOOLEAN",
        group="MAIN",
        settings_key="main_add_afisha",
        boolean=True,
        description="Отображение афиши на главной страницы",
    )
    Setting.objects.create(
        field_type="BOOLEAN",
        group="MAIN",
        settings_key="main_add_banners",
        boolean=True,
        description="Отображение банера на главной страницы",
    )
    Setting.objects.create(
        field_type="BOOLEAN",
        group="MAIN",
        settings_key="main_add_blog",
        boolean=True,
        description="Отображение дневника на главной страницы",
    )
    Setting.objects.create(
        field_type="BOOLEAN",
        group="MAIN",
        settings_key="main_add_news",
        boolean=True,
        description="Отображение новостей на главной страницы",
    )
    Setting.objects.create(
        field_type="BOOLEAN",
        group="MAIN",
        settings_key="main_add_places",
        boolean=True,
        description="Отображение площадок на главной страницы",
    )
    Setting.objects.create(
        field_type="BOOLEAN",
        group="MAIN",
        settings_key="main_add_short_list",
        boolean=True,
        description="Отображение шорт-листа на главной страницы",
    )
    Setting.objects.create(
        field_type="BOOLEAN",
        group="MAIN",
        settings_key="main_add_video_archive",
        boolean=True,
        description="Отображение видео-архива на главной страницы",
    )
    Setting.objects.create(
        field_type="TEXT",
        group="MAIN",
        settings_key="main_blog_title",
        text="Дневник фестиваля",
        description="Заголовок для дневника на главной страницы",
    )
    Setting.objects.create(
        field_type="TEXT",
        group="MAIN",
        settings_key="main_news_title",
        text="Новости",
        description="Заголовок для новостей на главной страницы",
    )
    Setting.objects.create(
        field_type="TEXT",
        group="MAIN",
        settings_key="main_short_list_title",
        text="Шорт-лист 2020 года",
        description="Заголовок для шорт-листа на главной страницы",
    )
    Setting.objects.create(
        field_type="BOOLEAN",
        group="MAIN",
        settings_key="main_show_afisha_only_for_today",
        boolean=True,
        description="Отображение афиши только на сегодня (в противном случае " "на ближайшие 6 дней)",
    )
    Setting.objects.create(
        field_type="IMAGE",
        group="MAIN",
        settings_key="main_video_archive_photo",
        image="core/2021-09-30_14.37.56.jpg",
        description="Фото для видео-архива на главной страницы",
    )
    Setting.objects.create(
        field_type="URL",
        group="MAIN",
        settings_key="main_video_archive_url",
        url="https://lubimovks.url.ru",
        description="Ссылка на youtube видео-архива на главной страницы",
    )

def add_short_list_program(apps, schema_editor):
    Program = apps.get_model('library', 'ProgramType')
    Program.objects.create(
        name="Шорт-лист",
        slug="short-list"
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(
            set_default_groups,
        ),
        migrations.RunPython(
            create_roles,
        ),
        migrations.RunPython(
            create_role_types,
        ),
        migrations.RunPython(
            add_types_to_roles,
        ),
        migrations.RunPython(
            add_email_settings,
        ),
        migrations.RunPython(
            add_afisha_settings,
        ),
        migrations.RunPython(
            add_first_screen_settings,
        ),
        migrations.RunPython(
            add_general_settings,
        ),
        migrations.RunPython(
            add_main_settings,
        ),
        migrations.RunPython(
            add_short_list_program,
        ),
    ]
