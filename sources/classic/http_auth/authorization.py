import functools

from . import errors
from .spec import Specification


def authorize(spec: Specification):
    def decorator(func):
        resource_name = func.__qualname__

        @functools.wraps(func)
        def wrapper(controller, request, response):
            client = request.context.client

            if not spec.is_satisfied_by(client):
                raise errors.PermissionDenied(resource_name=resource_name)

            result = func(controller, request, response)
            return result

        return wrapper

    return decorator
