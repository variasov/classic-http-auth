from typing import Any, Dict, Optional, Sequence, Type

try:
    import jwt
except ImportError:
    pass

try:
    import cryptography
except ImportError:
    pass

from classic.http_auth import errors, interfaces
from classic.http_auth.entities import Client

from .base import BaseStrategy


class KeycloakClientFactory(interfaces.ClientFactory):
    def get_client_cls(self) -> Type[Client]:
        return Client

    def create(self, **instance_params) -> Client:
        return self.get_client_cls().create(
            user_id=instance_params.get('sub'),
            login=instance_params.get('preferred_username'),
            name=instance_params.get('name'),
            groups=instance_params.get('groups'),
            email=instance_params.get('email'),
            app_groups=instance_params.get('app_groups'),
        )


class KeycloakOpenId(BaseStrategy):
    default_client_factory = KeycloakClientFactory()
    default_decoding_options = {'verify_signature': True, 'verify_aud': False, 'exp': True}

    def __init__(
        self,
        *,
        public_key: str = '',
        algorithms: Sequence[str] = None,
        decoding_options: Optional[Dict[str, Any]] = None,
        is_wrap_key=True,
        **kwargs
    ):
        try:
            jwt
        except NameError:
            raise AssertionError('Package pyjwt should be installed')

        try:
            cryptography
        except NameError:
            raise AssertionError('Package cryptography should be installed')

        super().__init__(**kwargs)

        self.algorithms = algorithms or ['RS256']
        self.public_key = self._prepare_public_key(public_key, is_wrap_key)
        self.decoding_options = self.default_decoding_options.copy()
        self.decoding_options.update(decoding_options or {})

        if not self.public_key:
            self.decoding_options['verify_signature'] = False

    def _prepare_public_key(self, public_key: str, is_wrap_key: bool):
        if not public_key:
            is_wrap_key = False

        return (
            f'-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----'
            if is_wrap_key else public_key
        )

    def _get_client_data(self, request: 'falcon.Request') -> Dict[str, Any]:
        if not request.auth:
            raise errors.AuthenticationError('No auth info in a request')

        parts = request.auth.split(' ')
        access_token = parts[-1]

        try:
            client_data = jwt.decode(
                access_token,
                self.public_key,
                algorithms=self.algorithms,
                options=self.decoding_options,
            )
        except jwt.DecodeError:
            raise errors.AuthenticationError('Token decoding error')
        except jwt.PyJWTError as e:
            raise errors.AuthenticationError(f'Unexpected token error [{str(e)}]')
        else:
            return client_data
