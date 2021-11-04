from functools import wraps
from typing import Any


def check_restriction(models: list[Any], error_msg_ending: str):
    model_names = [model.__qualname__ for model in models]
    required_instances = ", ".join(model_names)
    error_msg = (
        f"You should create at least one {required_instances} "
        f"before use {error_msg_ending}"
    )
    for model in models:
        assert model.objects.first(), error_msg


def restrictions(checks: dict[str, list[Any]]):
    """
    Check if instances of required models exist before use the fabric.

    How to use:
    The decorator takes a dictionary as a parameter.
    The keys of this dictionary are post_generation methods
    that can only be used if there are related model instances.
    Values is a list of models whose instances must exist in order
    to use the tested method.

    The decorator is applied to the create() and create_batch()
    factory methods.

    Use the 'global' key if the related model instances are required
    for the entire factory to work corretly.

    Example:
    class AuthorFactory(factory.django.DjangoModelFactory):

        ...

        @classmethod
        @restrictions({"add_play": [Festival, ProgramType]})
        def create(cls, **kwargs):
            return super().create(**kwargs)
    """

    def decorator(method):
        @wraps(method)
        def wrapped(*args, **kwargs):
            base_error_msg_ending = f"{method.__qualname__}()"
            if "global" in checks:
                check_restriction(checks.pop("global"), base_error_msg_ending)
            for arg, models in checks.items():
                is_arg = kwargs.get(arg)
                if not is_arg:
                    continue
                ending = base_error_msg_ending + f" with {arg}=True"
                check_restriction(models, ending)
            return method(*args, **kwargs)

        return wrapped

    return decorator
