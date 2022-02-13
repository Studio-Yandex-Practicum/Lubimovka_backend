from typing import Callable, Iterable, Optional

from django.db.models import Model


def restrict_factory(
    general: Optional[Iterable[Model]] = None,
    **params_restrictions: Iterable[Model],
) -> Callable:
    """Check if instances of required models exist before using the factory.

    Parameters:
    1. `general`: wait for the iterable of django `Model`. If set the decorator
    check whether even one object of the model exists.
    2. `**params_restrictions`: keyword variables. Each variable has to be
    iterable of django `Model`. The decorator checks whether at least one
    object of the model exists before running `Factory(variable)`.

    Examples:
    1. @restrict_factory(general: (Festival, ProgramType))
        class AuthorFactory(factory.django.DjangoModelFactory):
        ...
    In this case the decorator checks for one `Festival` and `Program_Type` in
    database before every call.

    2. @restrict_factory(
        general=(Festival, ProgramType),
        add_play=(Play,)
        )
        class AuthorFactory(factory.django.DjangoModelFactory):
        ...
    In this case the decorator
    - checks for one `Festival` and `Program_Type` in database before call
    - checks for `Play` object if `add_play` parameter was used

    3. @restrict_factory(add_play=(Play,))
        class AuthorFactory(factory.django.DjangoModelFactory):
        ...
    In this case:
    - AuthorFactory() runs without restrictions
    - AuthorFactory(add_play=True) will prohibited to run if there is no
    `Play` objects in database.
    """
    general_restrictions = general

    def check_restriction(
        models: Iterable[Model],
        factory_name: str,
        param: str = "",
    ) -> None:
        """Check is there at least one object of models exists. Assert if none."""
        model_names = [model.__qualname__ for model in models]
        required_instances = ", ".join(model_names)
        error_msg = f"You should create at least one {required_instances} before use {factory_name}({param})"
        for model in models:
            assert model.objects.exists(), error_msg

    def process_global_restrictions(
        factory_name: str,
        general_restrictions: Optional[Iterable[Model]],
    ) -> None:
        """Process restriction for the whole factory."""
        if general_restrictions is not None:
            models = general_restrictions
            check_restriction(models, factory_name)

    def process_parameters_restrictions(
        factory_name: str,
        params_restrictions: Optional[Iterable[Model]],
        called_params: str,
    ) -> None:
        """Process restriction for the the used parameters during factory call."""
        for param in called_params:
            if param in params_restrictions:
                models = params_restrictions[param]
                check_restriction(models, factory_name, param)

    def decorator(klass):
        class Factory(klass):
            @classmethod
            def _generate(cls, strategy, params):
                factory_name = klass.__name__
                process_global_restrictions(factory_name, general_restrictions)
                process_parameters_restrictions(factory_name, params_restrictions, params)
                return super()._generate(strategy, params)

        return Factory

    return decorator
