from abc import ABC, abstractmethod
from typing import Type

from .entities import Client

# yapf: disable


class AuthStrategy(ABC):
    @abstractmethod
    def get_client(self, request: 'falcon.Request', **static_client_params) -> Client: ...


class ClientFactory(ABC):
    @abstractmethod
    def get_client_cls(self) -> Type[Client]: ...

    @abstractmethod
    def create(self, **instance_params) -> Client: ...


# yapf: enable
