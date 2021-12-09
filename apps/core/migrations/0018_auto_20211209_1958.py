# Generated by Django 3.2.9 on 2021-12-09 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_data_add_type_roles'),
    ]

    operations = [
        migrations.RenameModel('Settings', 'Setting'),
        migrations.AlterModelOptions(
            name='setting',
            options={'ordering': ('group', 'settings_key'),
                     'verbose_name': 'Общие настройки',
                     'verbose_name_plural': 'Общие настройки'},
        ),
        migrations.AddField(
            model_name='setting',
            name='group',
            field=models.CharField(
                choices=[('EMAIL', 'Почта'), ('MAIN', 'Главная'),
                         ('FIRST_SCREEN', 'Первая страница'),
                         ('GENERAL', 'Общие')], default='GENERAL',
                max_length=50, verbose_name='Группа настроек'),
        ),
    ]
