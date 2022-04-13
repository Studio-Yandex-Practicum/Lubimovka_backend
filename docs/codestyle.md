# Общие правила

1. Придерживаемся [black style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)
2. f-строки предпочтительнее функции или выражений форматирования:\
    Т.е. **так плохо**
    ```python
    def __str__(self):
        return "{} {}".format(self.name, self.type)
    ```
    Так **хорошо**
    ```python
    def __str__(self):
         return f"{self.name} - {self.type}"
    ```
3. По возможности используем кортежи вместо списков. Кортеж - неизменяемый объект. [Вот тут про различия](https://www.educative.io/edpresso/tuples-vs-list-in-python)
    Т.е. **так не нужно**
    ```
    filterset_fields = ["year"]
    ```
    Лучше **так**
    ```
    filterset_fields = ("year",)
    ```


### Правила для моделей
1. Если хотя бы одно одно описание поля не помещается на одну строку, то для всех атрибутов полей используйте выделенную строку. \
    T.e **так плохо**
    ```python
    first_field = models.ForeignKey(Person, on_delete=models.PROTECT)
    second_field = models.CharField(
        max_length=200,
        unique=True,
    )
    ```
    Так **хорошо**
    ```python
    first_field = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
    )
    second_field = models.CharField(
        max_length=200,
        unique=True,
    )
    ```
2. У модели всегда должен присутствовать метод `__str__`
3. У каждой модели должно быть `verbose_name` и `verbose_name_plural`


### Правила для регистрации моделей в админке
1. Для регистрации моделей в админке используем декоратор ([документация](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#the-register-decorator)) \
    T.e **так плохо**
    ```python
    from django.contrib import admin
    from .models import Author


    class AuthorAdmin(admin.ModelAdmin):
        pass

    admin.site.register(Author, AuthorAdmin)
    ```
    Так **хорошо**
    ```python
    from django.contrib import admin
    from .models import Author


    @admin.register(Author)
    class AuthorAdmin(admin.ModelAdmin):
        pass
    ```


### Правила регистрации вычисляемых свойств на списке объектов в админке
1. При добавлении вычисляемых полей используем декоратор ([документация](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.display)) \
    T.e **так плохо**
    ```python
    def countable_field(self, obj):
        return True

    countable_field.short_description = "Поле"
    ```
    Так **хорошо**
    ```python
    @admin.display(
        boolean=True,
        ordering='-publish_date',
        description='Поле',
    )
    def countable_field(self, obj):
        return True
    ```


### Правило для получения настроек из settings
1. Для получения глобальных настроек из settings к полям обращаемся через сам settings\
    T.e **так плохо**
    ```python
   from config.settings.base import MAILJET_TEMPLATE_ID_PLAY

   message.template_id = MAILJET_TEMPLATE_ID_QUESTION
    ```
    Так **хорошо**
    ```python
   from django.conf import settings

   message.template_id = settings.MAILJET_TEMPLATE_ID_QUESTION
    ```
