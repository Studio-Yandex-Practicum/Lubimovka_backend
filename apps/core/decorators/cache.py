import time
from collections import namedtuple
from functools import wraps


def cache_user(timelimit):
    """Cache data for timelimit (in seconds)."""

    def cache_user_decorator(func):
        cache_user_dict = dict()
        named_tuple = namedtuple("named_tuple", "result, time")

        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            user = request.user.username
            current_time = time.time()
            if user in cache_user_dict and (current_time - cache_user_dict[user].time) < timelimit:
                return cache_user_dict[user].result
            result = func(self, request, *args, **kwargs)
            cache_user_dict[user] = named_tuple(result, current_time)
            return result

        return wrapper

    return cache_user_decorator
