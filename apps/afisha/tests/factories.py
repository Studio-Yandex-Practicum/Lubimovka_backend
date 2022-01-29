import factory
import pytz

from ..models import CommonEvent, Event


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    common_event = factory.Iterator(CommonEvent.objects.all())
    date_time = factory.Faker(
        "date_time_this_year",
        before_now=False,
        after_now=True,
        tzinfo=pytz.UTC,
    )
    paid = factory.Faker("boolean", chance_of_getting_true=50)
    url = factory.Faker("url")
    place = factory.Faker("address", locale="ru_RU")
    pinned_on_main = factory.Faker("boolean", chance_of_getting_true=80)
