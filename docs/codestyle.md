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
