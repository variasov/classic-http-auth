import collections
import functools
import logging
import traceback
from typing import Optional, Sequence, Union

try:
    import falcon
except ImportError:
    pass

from . import errors, interfaces
from .entities import Client


class Authenticator:
    def __init__(self, app_groups: Optional[Sequence["Group"]] = None):
        try:
            falcon
        except NameError:
            raise AssertionError('Dependency falcon should be installed')

        self.logger = logging.getLogger(f'http_auth.{self.__class__.__name__}')
        self.strategies = ()
        self.app_groups = tuple(app_groups) if app_groups else ()

    def set_strategies(
        self,
        strategies: Union[interfaces.AuthStrategy, Sequence[interfaces.AuthStrategy]],
    ):
        self.strategies = (
            tuple(strategies) if isinstance(strategies, collections.Sequence) else (strategies, )
        )

    def _try_to_get_client(
        self,
        request: falcon.Request,
        strategy: interfaces.AuthStrategy,
    ) -> Optional[Client]:
        client = None
        strategy_name = strategy.__class__.__name__

        try:
            client = strategy.get_client(request, app_groups=self.app_groups)
        except errors.AuthenticationError:
            self.logger.warning(
                'Error occurred on receive client info via strategy [%s]: %s',
                strategy_name,
                traceback.format_exc(),
            )
        if client:
            self.logger.debug('Client received')
        else:
            self.logger.debug('No client received by strategy [%s]', strategy_name)

        return client

    def auth(self, request: falcon.Request, resource_name: str = ""):
        client = None

        for strategy in self.strategies:
            client = self._try_to_get_client(request, strategy)
            if client:
                break

        if not client:
            raise errors.AuthenticationIsNotAvailable(resource_name=resource_name)

        request.context.client = client


def authenticator_needed(cls):
    old_cls_init = cls.__init__

    def new_init(instance, authenticator: Authenticator, *args, **kwargs):
        instance.authenticator = authenticator

        old_cls_init(instance, *args, **kwargs)

    cls.__annotations__['authenticator'] = Authenticator

    if getattr(cls, '__component__', False):
        cls.__init__ = new_init
    return cls


def authenticate(func):
    @functools.wraps(func)
    def wrapper(controller, request, response):
        authenticator = controller.authenticator

        resource_name = func.__qualname__
        authenticator.auth(request, resource_name)

        result = func(controller, request, response)
        return result

    return wrapper
