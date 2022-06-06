import random
from zoneinfo import ZoneInfo

import factory
from django.conf import settings

from apps.afisha.models import CommonEvent, Event
from apps.core.constants import YOUTUBE_VIDEO_LINKS
from apps.core.decorators import restrict_factory


@restrict_factory(general=(CommonEvent,))
class EventFactory(factory.django.DjangoModelFactory):
    """Create Event.

    Parameters:
    1. `date_time_in_three_hours=True`: create event at random time but not
    more than 3 hours from now.
    2. `masterclass=True`: bind event with random `master class`
    3. `reading=True`: bind event with random `reading`
    4. `performance=True`: bind event with random `performance`.
    """

    class Meta:
        model = Event

    class Params:
        date_time_in_three_hours = factory.Trait(
            date_time=factory.Faker(
                "future_datetime",
                end_date="+3h",
                tzinfo=ZoneInfo(settings.TIME_ZONE),
            ),
        )
        masterclass = factory.Trait(
            common_event=factory.LazyFunction(
                lambda: CommonEvent.objects.exclude(masterclass__isnull=True).order_by("?").first()
            ),
        )
        reading = factory.Trait(
            common_event=factory.LazyFunction(
                lambda: CommonEvent.objects.exclude(reading__isnull=True).order_by("?").first()
            ),
        )
        performance = factory.Trait(
            common_event=factory.LazyFunction(
                lambda: CommonEvent.objects.exclude(performance__isnull=True).order_by("?").first()
            ),
        )

    date_time = factory.Faker(
        "date_time_this_year",
        before_now=False,
        after_now=True,
        tzinfo=ZoneInfo(settings.TIME_ZONE),
    )
    paid = factory.Faker("boolean", chance_of_getting_true=50)
    url = factory.LazyFunction(lambda: random.choice(YOUTUBE_VIDEO_LINKS))
    place = factory.Faker("address", locale="ru_RU")
    pinned_on_main = factory.Faker("boolean", chance_of_getting_true=80)

    @factory.lazy_attribute
    def common_event(self):
        return CommonEvent.objects.order_by("?").first()
