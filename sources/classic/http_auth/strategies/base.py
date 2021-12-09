from abc import abstractmethod
from typing import Any, Dict

from classic.http_auth import interfaces
from classic.http_auth.entities import Client


class BaseStrategy(interfaces.AuthStrategy):
    default_client_factory = None

    def __init__(self, client_factory: interfaces.ClientFactory = None):
        self.client_factory = client_factory or self.default_client_factory

    def get_client(self, request: 'falcon.Request', **static_client_params) -> Client:
        client_data = self._get_client_data(request)
        return self.client_factory.create(**client_data, **static_client_params)

    @abstractmethod
    def _get_client_data(self, request: 'falcon.Request') -> Dict[str, Any]:
        ...
