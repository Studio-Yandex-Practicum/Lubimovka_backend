# Generated by Django 3.2.11 on 2022-01-29 09:53

import apps.library.utilities
import apps.library.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    replaces = [('library', '0003_auto_20211013_0054'), ('library', '0004_added_model_performance'), ('library', '0005_auto_20211017_2001_squashed_0010_auto_20211022_2025'), ('library', '0006_updated_performance'), ('library', '0006_auto_20211024_0733_squashed_0007_auto_20211025_1939'), ('library', '0007_merge_20211027_1905'), ('library', '0008_auto_20211028_2106'), ('library', '0009_alter_author_options')]

    dependencies = [
        ('core', '0002'),
        ('afisha', '0002'),
        ('library', '0001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ('-created',), 'verbose_name': 'Спектакль', 'verbose_name_plural': 'Спектакли'},
        ),
        migrations.AddField(
            model_name='performance',
            name='bottom_image',
            field=models.ImageField(default=None, upload_to='performances/', verbose_name='Изображение внизу страницы'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='performance',
            name='event',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='performances', to='afisha.commonevent', verbose_name='Базовое событие'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='performance',
            name='main_image',
            field=models.ImageField(default=None, upload_to='performances/', verbose_name='Главное изображение'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='performance',
            name='play',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='performances', to='library.play', verbose_name='Пьеса'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='performance',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название спектакля'),
        ),
        migrations.AddField(
            model_name='performance',
            name='description',
            field=models.TextField(default=None, max_length=500, verbose_name='Краткое описание'),
        ),
        migrations.AddField(
            model_name='performance',
            name='text',
            field=models.TextField(default=None, verbose_name='Полное описание'),
        ),
        migrations.RemoveField(
            model_name='author',
            name='authors_plays_links',
        ),
        migrations.AddField(
            model_name='author',
            name='author_plays_links',
            field=models.ManyToManyField(blank=True, related_name='authors_links', to='library.Play', verbose_name='Ссылки на пьесы автора'),
        ),
        migrations.AlterField(
            model_name='author',
            name='achievements',
            field=models.ManyToManyField(blank=True, to='library.Achievement', verbose_name='Достижения'),
        ),
        migrations.AlterField(
            model_name='author',
            name='other_links',
            field=models.ManyToManyField(blank=True, related_name='authors', to='library.OtherLink', verbose_name='Ссылки на внешние ресурсы'),
        ),
        migrations.AlterField(
            model_name='author',
            name='social_network_links',
            field=models.ManyToManyField(blank=True, related_name='authors', to='library.SocialNetworkLink', verbose_name='Ссылки на социальные сети'),
        ),
        migrations.AddField(
            model_name='performance',
            name='age_limit',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(18)], verbose_name='Возрастное ограничение'),
        ),
        migrations.AddField(
            model_name='performance',
            name='video',
            field=models.URLField(blank=True, unique=True, verbose_name='Видео'),
        ),
        migrations.RemoveField(
            model_name='masterclass',
            name='director',
        ),
        migrations.RemoveField(
            model_name='masterclass',
            name='dramatist',
        ),
        migrations.AddField(
            model_name='performance',
            name='images_in_block',
            field=models.ManyToManyField(blank=True, to='core.Image', verbose_name='Фотографии спектакля в блоке фотографий'),
        ),
        migrations.AlterField(
            model_name='play',
            name='city',
            field=models.CharField(max_length=200, verbose_name='Город'),
        ),
        migrations.CreateModel(
            name='PerformancePerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('role', models.CharField(choices=[('Actor', 'Актёр'), ('Adapter', 'Адаптация текста'), ('Dramatist', 'Драматург'), ('Director', 'Режиссёр'), ('Interpreter', 'Переводчик')], max_length=200, verbose_name='Роль в команде спектакля')),
                ('performance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performance_persons', to='library.performance', verbose_name='Спектакль')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='performance_persons', to='core.person', verbose_name='Член команды')),
            ],
            options={
                'verbose_name': 'Член команды',
                'verbose_name_plural': 'Члены команды',
                'ordering': ('role',),
            },
        ),
        migrations.AddField(
            model_name='performance',
            name='persons',
            field=models.ManyToManyField(related_name='performances', through='library.PerformancePerson', to='core.Person', verbose_name='Члены команды'),
        ),
        migrations.CreateModel(
            name='ParticipationApplicationFestival',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('birthday', models.DateField(verbose_name='День рождения')),
                ('city', models.CharField(max_length=50, verbose_name='Город проживания')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('email', models.EmailField(max_length=100, verbose_name='Электронная почта')),
                ('title', models.CharField(max_length=200, verbose_name='Название пьесы')),
                ('year', models.PositiveSmallIntegerField(validators=[apps.library.validators.year_validator], verbose_name='Год написания')),
                ('file', models.FileField(upload_to=apps.library.utilities.generate_class_name_path, validators=[django.core.validators.FileExtensionValidator(['doc', 'docx', 'txt', 'odt', 'pdf'])], verbose_name='Файл')),
                ('verified', models.BooleanField(choices=[(True, 'Да'), (False, 'Нет')], default=False, verbose_name='Проверена?')),
            ],
            options={
                'verbose_name': 'Заявление на участие',
                'verbose_name_plural': 'Заявления на участие',
            },
        ),
        migrations.AddConstraint(
            model_name='participationapplicationfestival',
            constraint=models.UniqueConstraint(fields=('first_name', 'last_name', 'birthday', 'city', 'phone_number', 'email', 'title', 'year'), name='unique_application'),
        ),
        migrations.RemoveField(
            model_name='author',
            name='author_plays_links',
        ),
        migrations.RemoveField(
            model_name='author',
            name='other_links',
        ),
        migrations.RemoveField(
            model_name='author',
            name='other_plays_links',
        ),
        migrations.RemoveField(
            model_name='author',
            name='social_network_links',
        ),
        migrations.RemoveField(
            model_name='play',
            name='authors',
        ),
        migrations.AddField(
            model_name='author',
            name='plays',
            field=models.ManyToManyField(blank=True, related_name='authors', to='library.Play', verbose_name='Пьесы автора'),
        ),
        migrations.AlterField(
            model_name='author',
            name='achievements',
            field=models.ManyToManyField(blank=True, related_name='authors', to='library.Achievement', verbose_name='Достижения'),
        ),
        migrations.AlterField(
            model_name='author',
            name='person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.person', verbose_name='Человек'),
        ),
        migrations.AlterField(
            model_name='otherlink',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='other_links', to='library.author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='otherplay',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='other_plays', to='library.author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='play',
            name='url_download',
            field=models.URLField(blank=True, null=True, unique=True, verbose_name='Ссылка на скачивание пьесы'),
        ),
        migrations.AlterField(
            model_name='play',
            name='url_reading',
            field=models.URLField(blank=True, null=True, unique=True, verbose_name='Ссылка на читку'),
        ),
        migrations.AlterField(
            model_name='play',
            name='year',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1990), django.core.validators.MaxValueValidator(2021)], verbose_name='Год написания пьесы'),
        ),
        migrations.AlterField(
            model_name='socialnetworklink',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_networks', to='library.author', verbose_name='Автор'),
        ),
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['person__last_name'], 'verbose_name': 'Автор', 'verbose_name_plural': 'Авторы'},
        ),
    ]
