from functools import wraps
from typing import Any


def check_restriction(models: list[Any], factory_info: str):
    model_names = [model.__qualname__ for model in models]
    required_instances = ", ".join(model_names)
    error_msg = (
        f"You should create at least one {required_instances} "
        f"before use {factory_info}"
    )
    for model in models:
        assert model.objects.first(), error_msg


def restrict_factory_method(restrictions: dict[str, list[Any]]):
    def decorator(method):
        @wraps(method)
        def wrapped(*args, **kwargs):
            factory_name = restrictions.pop("_factory_name")
            if "global" in restrictions:
                models = restrictions.pop("global")
                check_restriction(models, factory_name)
            method_keyword_variables = kwargs
            for keyword_variable in method_keyword_variables:
                if keyword_variable in restrictions:
                    models = restrictions[keyword_variable]
                    factory_info = (
                        factory_name + f" with {keyword_variable}=True"
                    )
                    check_restriction(models, factory_info)
            return method(*args, **kwargs)

        return wrapped

    return decorator


def restrict_factory(restrictions: dict[str, list[Any]]):
    """
    Checks if instances of required models exist before use the fabric.

    How to use:
    The decorator takes a dictionary as a parameter.
    The keys of this dictionary are post_generation methods
    that can only be used if there are related model instances.
    Values is a list of models whose instances must exist in order
    to use the tested method.

    The decorator is applied to fabric class and expands create classmethod
    with necessary checks.

    Use the 'global' key if the related model instances are required
    for the entire factory to work correctly.

    Example:

    @restrict_factory({"add_play": [Festival, ProgramType]})
    class AuthorFactory(factory.django.DjangoModelFactory):
        @factory.post_generation
        def add_play(self, created, extracted, **kwargs):
            '''
            Create a Play object and add it to other_plays_links
            field for Author.
            You should create at least one Festival and Program
            before use this method.
            To use "add_play=True"
            '''
            if not created:
                return
            if extracted:
                play = PlayFactory.create()
                self.plays.add(play)
    """

    def decorator(klass):
        restrictions.update({"_factory_name": klass.__name__})

        class Factory(klass):
            @classmethod
            @restrict_factory_method(restrictions)
            def create(cls, **kwargs):
                return super().create(**kwargs)

        return Factory

    return decorator
