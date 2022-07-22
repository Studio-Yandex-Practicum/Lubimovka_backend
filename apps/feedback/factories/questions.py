import factory
from faker import Faker

from apps.feedback.models import Question

fake = Faker("ru_RU")


class QuestionFactory(factory.django.DjangoModelFactory):
    """Create Question objects."""

    class Meta:
        model = Question

    author_name = factory.Faker("first_name", locale="ru_RU")
    author_email = factory.Faker("email")
    question = factory.Faker("text", max_nb_chars=500, locale="ru_RU")
