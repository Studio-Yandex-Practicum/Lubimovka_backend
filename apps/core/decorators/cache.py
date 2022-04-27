import time
from collections import namedtuple
from functools import wraps


def decorator_with_args(decorator_to_enhance):
    """Needs only for other decorator to add some arguments."""

    def decorator_maker(*args, **kwargs):
        def decorator_wrapper(func):
            return decorator_to_enhance(func, *args, **kwargs)

        return decorator_wrapper

    return decorator_maker


@decorator_with_args
def cache_user(func, *args, **kwargs):
    """Cache data for timelimit (in seconds)."""
    cache_user_dict = dict()
    timelimit = kwargs["timelimit"]
    named_tuple = namedtuple("named_tuple", "result, time")

    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        user = request.user.username
        current_time = round(time.time() / timelimit)
        if user in cache_user_dict and current_time == cache_user_dict[user].time:
            return cache_user_dict[user].result
        result = func(self, request, *args, **kwargs)
        cache_user_dict[user] = named_tuple(result, current_time)
        return result

    return wrapper
