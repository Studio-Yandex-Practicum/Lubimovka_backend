from zoneinfo import ZoneInfo

import factory
from django.conf import settings

from apps.afisha.models import CommonEvent, Event


class EventFactory(factory.django.DjangoModelFactory):
    """Create Event.

    Parameters:
    1.`date_time_in_three_hours=True`: create event at random time but not
    more than 3 hours from now.
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

    date_time = factory.Faker(
        "date_time_this_year",
        before_now=False,
        after_now=True,
        tzinfo=ZoneInfo(settings.TIME_ZONE),
    )
    paid = factory.Faker("boolean", chance_of_getting_true=50)
    url = factory.Faker("url")
    place = factory.Faker("address", locale="ru_RU")
    pinned_on_main = factory.Faker("boolean", chance_of_getting_true=80)

    @factory.lazy_attribute
    def common_event(self):
        return CommonEvent.objects.order_by("?").first()
