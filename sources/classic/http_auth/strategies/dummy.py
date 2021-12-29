from typing import Any, Dict, Type

from classic.http_auth import Client, interfaces
from classic.http_auth.strategies.base import BaseStrategy


class DummyClientFactory(interfaces.ClientFactory):
    def get_client_cls(self) -> Type[Client]:
        return Client

    def create(self, **instance_params) -> Client:
        return self.get_client_cls().create(
            user_id=instance_params.get('user_id'),
            login=instance_params.get('login'),
            name=instance_params.get('name'),
            groups=instance_params.get('groups'),
            email=instance_params.get('email'),
            app_groups=instance_params.get('app_groups'),
        )


class Dummy(BaseStrategy):
    default_client_factory = DummyClientFactory()

    def __init__(self, client_factory: interfaces.ClientFactory = None, **client_params):
        self.client_params = client_params

        super().__init__(client_factory=client_factory)

    def _get_client_data(self, request: 'falcon.Request') -> Dict[str, Any]:
        return self.client_params
