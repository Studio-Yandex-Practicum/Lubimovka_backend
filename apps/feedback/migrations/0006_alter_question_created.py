# Generated by Django 3.2.21 on 2023-11-14 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0005_alter_participationapplicationfestival_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создан'),
        ),
    ]