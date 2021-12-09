from dataclasses import dataclass
from typing import Callable

from .authentication import Authenticator, authenticate, authenticator_needed
from .authorization import authorize
from .entities import Client, Group, Permission


@dataclass
class AaaNs:
    authenticate: Callable
    authorize: Callable
    authenticator_needed: Callable


aaa = AaaNs(authenticate, authorize, authenticator_needed)

__all__ = [
    "Authenticator",
    "Client",
    "Group",
    "Permission",
    "aaa",
]
