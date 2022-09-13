import random
from zoneinfo import ZoneInfo

import factory
from django.conf import settings

from apps.afisha.models import CommonEvent, Event
from apps.core.decorators import restrict_factory
from apps.info.utils import get_random_objects_by_model, get_random_objects_by_queryset
from apps.library.factories.constants import YOUTUBE_VIDEO_LINKS


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
                lambda: get_random_objects_by_queryset(CommonEvent.objects.exclude(masterclass__isnull=True))
            ),
        )
        reading = factory.Trait(
            common_event=factory.LazyFunction(
                lambda: get_random_objects_by_queryset(CommonEvent.objects.exclude(reading__isnull=True))
            ),
        )
        performance = factory.Trait(
            common_event=factory.LazyFunction(
                lambda: get_random_objects_by_queryset(CommonEvent.objects.exclude(performance__isnull=True))
            ),
        )

    date_time = factory.Faker(
        "date_time_this_year",
        before_now=False,
        after_now=True,
        tzinfo=ZoneInfo(settings.TIME_ZONE),
    )
    action = factory.Iterator(Event.ActionType.values)
    url = factory.LazyFunction(lambda: random.choice(YOUTUBE_VIDEO_LINKS))
    pinned_on_main = factory.Faker("boolean", chance_of_getting_true=80)

    @factory.lazy_attribute
    def common_event(self):
        return get_random_objects_by_model(CommonEvent)
