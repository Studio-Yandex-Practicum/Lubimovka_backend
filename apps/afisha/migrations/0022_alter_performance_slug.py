
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afisha', '0021_performance_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='slug',
            field=models.SlugField(error_messages={'unique': 'Такой транслит уже используется, введите иной'}, help_text='Формируется автоматически, может быть изменен вручную', max_length=200, unique=True, verbose_name='Транслит названия для формирования адресной строки'),
        ),
    ]
