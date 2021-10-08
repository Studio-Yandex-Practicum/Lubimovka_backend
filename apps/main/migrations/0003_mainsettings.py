# Generated by Django 3.2.7 on 2021-10-08 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0004_alter_person_image'),
        ('main', '0002_delete_mainpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('festival', models.BooleanField(verbose_name='Состояние Фестиваль или нет')),
                ('persons_how_get_questions', models.ManyToManyField(to='core.Person', verbose_name='Люди, получающие вопросы на почту')),
            ],
            options={
                'verbose_name': 'Основные настройки',
                'verbose_name_plural': 'Основные настройки',
            },
        ),
    ]
