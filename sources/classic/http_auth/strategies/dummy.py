from typing import Any, Dict, Optional, Set, Type

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

    def __init__(
        self,
        login: str,
        name: str,
        groups: Optional[Set] = None,
        email: Optional[str] = None,
        **kwargs,
    ):
        self.login = login
        self.name = name
        self.groups = groups
        self.email = email

        super().__init__(**kwargs)

    def _get_client_data(self, request: 'falcon.Request') -> Dict[str, Any]:
        return {
            'user_id': 1,
            'name': self.name,
            'login': self.login,
            'email': self.email,
            'groups': self.groups,
        }
