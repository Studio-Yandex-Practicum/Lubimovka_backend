# Generated by Django 3.2.11 on 2022-01-29 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('description', models.TextField(max_length=500, verbose_name='Описание')),
                ('url', models.URLField(verbose_name='Ссылка')),
                ('image', models.ImageField(upload_to='images/main/banner', verbose_name='Картинка')),
                ('button', models.CharField(choices=[('TICKETS', 'Билеты'), ('DETAILS', 'Подробнее'), ('READ', 'Читать')], max_length=40, verbose_name='Выбор типа кнопки')),
            ],
            options={
                'verbose_name': 'Банер для главной странице',
                'verbose_name_plural': 'Банеры для главной странице',
            },
        ),
        migrations.CreateModel(
            name='SettingAfishaScreen',
            fields=[
            ],
            options={
                'verbose_name': 'Настройки афиши',
                'verbose_name_plural': 'Настройки афиши',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.setting',),
        ),
        migrations.CreateModel(
            name='SettingEmail',
            fields=[
            ],
            options={
                'verbose_name': 'Настройки обратной связи',
                'verbose_name_plural': 'Настройки обратной связи',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.setting',),
        ),
        migrations.CreateModel(
            name='SettingFirstScreen',
            fields=[
            ],
            options={
                'verbose_name': 'Настройки первой страницы',
                'verbose_name_plural': 'Настройки первой страницы',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.setting',),
        ),
        migrations.CreateModel(
            name='SettingGeneral',
            fields=[
            ],
            options={
                'verbose_name': 'Общие настройки',
                'verbose_name_plural': 'Общие настройки',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.setting',),
        ),
        migrations.CreateModel(
            name='SettingMain',
            fields=[
            ],
            options={
                'verbose_name': 'Настройки главной страницы',
                'verbose_name_plural': 'Настройки главной страницы',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.setting',),
        ),
    ]
